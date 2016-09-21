import sys
import time
from Queue import Queue
from threading import *
from prettytable import PrettyTable
from termcolor import colored,cprint
from myhandler.socket_handler import *
from myhandler.packet_handler import *

sys.dont_write_bytecode=True

filtered   = Queue()
unfiltered = Queue()


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

class AckScan(object):
	def __init__(self,
		        mysock,
		        tgt,
		        dport,
		        packet,
		        catcher,
		        lock):
	    super(AckScan,self).__init__()
	    self.mysock  = mysock
	    self.tgt 	 = tgt
	    self.dport	 = dport
	    self.packet  = packet
	    self.catcher = catcher
	    self.lock 	 = lock
	    self.c  	 = 0

	def scan(self):
		try:
			self.mysock.sendto(self.packet,(self.tgt,0))
			packet = self.catcher.next()
			if packet == None:
				with self.lock:
					self.c+=1
					serv = getportserv(int(self.dport))
					data = (str(self.dport),'filtered',serv)
					filtered.put(data)
			else:
				extract_data = UnpackPacket(packet[1],None,None)
				data 		 = extract_data._unpackAckScan()
				if 'filtered' in data:
					filtered.put(data)
				else:
					unfiltered.put(data)
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
				with self.lock:
					serv = getportserv(int(self.port))
					print str(port).ljust(7)+'filtered'.ljust(12)+serv
			else:
				extract_data = UnpackPacket(packet[1],None,None)
				data 		 = extract_data._unpackAckScan()
				(port,state,serv) = data
				print str(port).ljust(7)+state.ljust(12)+serv
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))
		finally:
			pass

class ActiveAck:
	def __init__(self,tgt,prange,to):
		self.tgt     = gethostbyname(tgt)
		self.prange  = confirm_port_range(prange)
		self.to 	 = float(to)
		self.mysock  = create_tcp_socket(self.to,'')
		self.single  = False
		self.ouraddr = get_our_addr()

	def _start(self):

		t1 = match_time()

		if len(self.prange) == 1:
			for num in self.prange:
				port = num
				self.single == True
		else:
			srange = int(self.prange[0])
			erange = int(self.prange[1])+1

		setup_catcher = Catch_packet(self.tgt)
		catcher 	  = setup_catcher._set_tcp()

		s   		  = Semaphore(100)
		lock 		  = Lock()

		threads		  = []
		fp			  = []
		ufp 		  = []
		table 		  = PrettyTable(['PORT','STATE','SERVICE','REASOM'])

		if self.single == True:
			print 'PORT'.ljust(7)+'STATE'.ljust(12)+'SERVICE'
			builder = TCPPacket(self.tgt,
                                int(port),
                                self.ouraddr,
                                'ack')
			packet  = builder.building_packet()
			pool 	= AckScan(self.mysock,
                              self.tgt,
                              port,
                              packet,
                              catcher,
                              lock)
			pool._AckScan.__single_scan()
		else:
			try:
				for dport in xrange(srange,erange):
					builder = TCPPacket(self.tgt,
                                        dport,
                                        self.ouraddr,
                                        'ack')
					packet  = builder.building_packet()
					pool    = AckScan(self.mysock,
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
					if not filtered.empty():
						data = filtered.get()
						fp.append(data)
					else:
						break
				while 1:
					if not unfiltered.empty():
						data = unfiltered.get()
						ufp.append(data)
					else:
						break

				if len(fp) == erange - srange:
					print 'All {0} scanned ports on {1} are filtered'.format(colored((len(fp) - 1),'red'),colored(self.tgt,'yellow'))
				elif len(ufp) == erange - srange:
					print 'All {0} scanned ports on {1} are unfiltered'.format(colored((len(ufp) - 1),'red'),colored(self.tgt,'yellow'))
				elif len(fp) < erange - srange:
					for data in fp:
						table.add_row(data)
					print table
				elif len(ufp) < erange - srange:
					for data in ufp:
						table.add_row(data)
					print table
			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user','red'))


		t2 = match_time()
		tt = t2 - t1
		print (colored('Collector finished scan in: ','blue')+colored('{} sec'.format(tt),'yellow')+'\n')

