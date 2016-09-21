import sys
import time
from threading import *
from Queue import Queue
from prettytable import *
from termcolor import colored,cprint
from myhandler.packet_handler import *
from myhandler.socket_handler import *
from myhandler.skip_port import SkipPort
sys.dont_write_bytecode=True

q=Queue()
f=Queue()

def match_time_sys():
	if sys.platform == 'linux2':
		return time.time()
	else:
		return time.clock()

def activeScanner(s,pool):
	try:
		with s:
			pool.scan()
	except KeyboardInterrupt:
		sys.exit(cprint('[-] Canceled by user','red'))

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


class StealthScan(object):
	def __init__(self,
		        mysock,
		        dip,
		        packet,
		        quite,
		        catcher,
		        PortSkipper,
		        locker):
	        super(StealthScan,self).__init__()
	        self.mysock      = mysock
	        self.dip         = dip
	        self.packet      = packet
	        self.quite       = quite
	        self.catcher     = catcher
	        self.PortSkipper = PortSkipper
	        self.lock        = locker
	        self.c           = 0

	def scan(self):
		try:
			self.mysock.sendto(self.packet,(self.dip,0))
			packet=self.catcher.next()
			if packet == None:
				f.put(1)
			else:
				with self.lock:
					self.c+=1
					d=UnpackPacket(packet[1],self.quite,self.PortSkipper)
					data=d._unpackTCP()
					if self.quite == False:
						(port,serv,state)=data
						re=(str(port).ljust(10)+serv.ljust(15)+state)
						print re
					else:
						q.put(data)
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))
		except:
			pass

class ActiveStealth:
	def __init__(self,tgt,prange,to,quite):
		self.tgt 	= tgt
		self.prange = confirm_port_range(prange)
		self.to 	= float(to)
		self.quite 	= quite
		self.mysock = create_tcp_socket(self.to,'syn')
		self.single = False

	def _get_dip(self):
		return resolve_host(self.tgt)

	def _start(self):
		t1 			  = match_time_sys()
		if len(self.prange) == 1:
			self.single = True
			for num in self.prange:
				port  = num
		else:
			srange    = int(self.prange[0])
			erange 	  = int(self.prange[1])

		sip 		  = get_our_addr()
		dip 		  = self._get_dip()

		PortSkipper   = SkipPort()
		setup_catcher = Catch_packet(dip)
		catcher 	  = setup_catcher._set_tcp()

		s 			  = Semaphore(100)
		locker        = Lock()

		field         = ['Port','Serv','Win','TTL','Reason']
		mytable       = PrettyTable(field)

		datas 		  = []
		threads       = []
		fports 		  = -1

		if self.single == True:
			fports   = 0
			builder  = TCPPacket(dip,int(port),sip,'syn')
			packet   = builder.building_packet()
			pool     = StealthScan(self.mysock,
                                   dip,
                                   packet,
                                   self.quite,
                                   catcher,
                                   PortSkipper,
                                   locker)
			t        = Thread(target=activeScanner,args=(s,pool))
			t.daemon = True
			t.start()
			t.join()
		else:
			try:
				for port in xrange(srange,erange):
					builder = TCPPacket(dip,port,sip,'syn')
					packet  = builder.building_packet()

					pool    = StealthScan(self.mysock,
                                          dip,
                                          packet,
                                          self.quite,
                                          catcher,
                                          PortSkipper,
                                          locker)
					t       = Thread(target=activeScanner,args=(s,pool))
					threads.append(t)

				for x in xrange(len(threads)):
					threads[x].daemon=True
					threads[x].start()

				for x in xrange(len(threads)):
					threads[x].join()
			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user','red'))

		while 1:
			if not q.empty():
				data=q.get()
				if data != None:
					datas.append(data)
			else:
				break

		while 1:
			if not f.empty():
				fp=f.get()
				fports+=fp
			else:
				break

		if self.quite == True:
			for data in datas:
				mytable.add_row(data)
			print mytable

		print '\nGot {} ports closed'.format(colored(fports,'cyan'))

		t2=match_time_sys()
		tt=t2-t1
		fs=(colored('Collector finished scan in: ','blue')+colored('{} sec'.format(tt),'yellow')+'\n')
		print(fs)


