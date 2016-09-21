import sys
import time
from threading import *
from Queue import Queue
from prettytable import PrettyTable
from termcolor import colored,cprint
from myhandler.socket_handler import *
from myhandler.packet_handler import *
sys.dont_write_bytecode=True

cp  = Queue()
ofp = Queue()

def active_pool(s,pool):
	with s:
		pool.scan()

def match_time():
	if sys.platform == 'linux2':
		return time.time()
	else:
		return time.clock()

def confirm_port_range(prange):
	fe=prange.count('-')
	if fe == 1:
		split_it = prange.split('-')
		try:
			if isinstance(int(split_it[0]),int) and isinstance(int(split_it[1]),int):
				pass
		except: 
			raise ValueError('Port range must be interger')
			sys.exit(1)
		if split_it[0] > split_it[1]:
			srange=split_it[1]
			erange=split_it[0]
		else:
			srange=split_it[0]
			erange=split_it[1]
		return (srange,erange)
	else:
		try:
			isinstance(int(prange),int)
		except:
			raise ValueError('Port must be interger')
			sys.exit(1)
		return [prange]

class NullScan(object):
	def __init__(self,
		        mysock,
		        tgt,
		        port,
		        packet,
		        catcher,
		        lock):
	    super(NullScan,self).__init__()
	    self.mysock  = mysock
	    self.tgt  	 = tgt
	    self.port    = port
	    self.packet  = packet
	    self.catcher = catcher
	    self.lock 	 = lock
	    self.c 		 = 0

	def scan(self):
		try:
			self.mysock.sendto(self.packet,(self.tgt,0))
			time.sleep(.3)
			packet = self.catcher.next()
			if packet == None:
				with self.lock:
					serv = getportserv(int(self.port))
					data = (str(self.port),'open|filtered',serv)
					ofp.put(data)
			else:
				d 	 = UnpackPacket(packet[1],None,None)
				data = d._unpackTCP()
				cp.put(data)
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))
		finally:
			pass

	def __single_scan(self):
		try:
			self.mysock.sendto(self.packet,(self.tgt,0))
			time.sleep(.7)
			packet = self.catcher.next()
			if packet == None:
				serv = getportserv(int(self.port))
				print str(self.port).ljust(7)+'open|filtered'.ljust(15)+serv
			else:
				print str(self.port).ljust(7)+'closed'.ljust(15)+serv
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))

class ActiveNull:
	def __init__(self,tgt,prange,to):
		self.tgt 	 = gethostbyname(tgt)
		self.prange  = confirm_port_range(prange)
		self.to 	 = float(to)
		self.mysock  = create_tcp_socket(self.to,'')
		self.ouraddr = get_our_addr()
		self.single  = False

	def _start(self):
		t1        = match_time()

		if len(self.prange) == 1:
			for num in self.prange:
				port = num
				self.single = True

		else:
			srange = int(self.prange[0])
			erange = int(self.prange[1])+1

		setup_catcher = Catch_packet(self.tgt)
		catcher 	  = setup_catcher._set_tcp()

		s 			  = Semaphore(100)
		lock		  = Lock()

		threads		  = []
		ofp_c 		  = []
		cp_c 		  = []
		table 		  = PrettyTable(['PORT','STATE','SERV'])

		if self.single == True:
			print 'PORT'.ljust(7)+'STATE'.ljust(15)+'SERVICE'
			builder = TCPPacket(self.tgt,
                                int(port),
                                self.ouraddr,
                                'null')
			packet  = builder.building_packet()
			pool    = NullScan(self.mysock,
                              self.tgt,
                              int(port),
                              packet,
                              catcher,
                              lock)
			pool._NullScan__single_scan()

		else:
			try:
				for dport in xrange(srange,erange):
					builder = TCPPacket(self.tgt,
                                        dport,
                                        self.ouraddr,
                                        'null')
					packet  = builder.building_packet()
					pool    = NullScan(self.mysock,
                                      self.tgt,
                                      dport,
                                      packet,
                                      catcher,
                                      lock)
					t 		= Thread(target=active_pool,args=(s,pool))
					threads.append(t)

				for thread in threads:
					thread.daemon = True
					thread.start()

				for thread in threads:
					thread.join()

				while 1:
					if not ofp.empty():
						data = ofp.get()
						if data != None:
							ofp_c.append(data)
					else:
						break
				while 1:
					if not cp.empty():
						data = cp.get()
						if data != None:
							cp_c.append(data)
					else:
						break

				cp_len  = len(cp_c)
				ofp_len = len(ofp_c)
				if cp_len == erange - srange:
					print 'All {0} scanned ports on {1} are closed'.format(colored((cp_len - 1),'red'),colored(self.tgt,'yellow'))
				elif ofp_len == erange - srange:
					print 'All {0} scanned ports on {1} are open|filtered'.format(colored((ofp_len - 1),'red'),colored(self.tgt,'yellow'))
				elif cp_len < erange - srange:
					for data in cp_c:
						table.add_row(data)
					print data
				elif ofp_len < erange - srange:
					for data in ofp_c:
						table.add_row(data)
					print data

			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user','red'))
			finally:
				pass

		t2 = match_time()
		tt = t2 - t1
		fs=(colored('Collector finished scan in: ','blue')+colored('{} sec'.format(tt),'yellow')+'\n')
		print fs
