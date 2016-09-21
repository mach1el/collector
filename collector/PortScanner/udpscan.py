import sys
import time
from random import *
from threading import *
from Queue import Queue
from prettytable import PrettyTable
from termcolor import cprint,colored
from myhandler.socket_handler import *
from myhandler.packet_handler import *
from myhandler.skip_port import SkipPort
from myhandler.CountPort import CountPort
sys.dont_write_bytecode=True

OFP         = Queue()
open_port   = Queue()
closed_port = Queue()

def catch_packet(catcher):
	return catcher.next()

def start_pool(s,pool):
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
	else:
		try:
			isinstance(int(prange),int)
		except:
			raise ValueError('Port must be interger')
		else:
			return [prange]

	return (srange,erange)


class UdpScanner(object):
	def __init__(self,
		        mysock,
		        dip,
		        port,
		        packet,
		        catcher,
		        locker,
		        counter,
		        skipper,
		        single):
		super(UdpScanner,self).__init__()
		self.mysock       = mysock
		self.dip          = dip
		self.port         = port
		self.packet       = packet
		self.catcher      = catcher
		self.locker       = locker
		self.counter      = counter
		self.skipper	  = skipper
		self.single       = single
		self.c            = 0

	def scan(self):
		try:
			if self.mysock.sendto(self.packet,(self.dip,0)):
				with self.locker:
					if self.single == True:
						time.sleep(.5)
						packet = catch_packet(self.catcher)
					else:
						packet = catch_packet(self.catcher)
					if packet == None:
						data = (self.port,getportserv(self.port),'None','open|filtered','not-response')
						OFP.put(data)
						self.counter.StartCount(0)
					else:
						recvPacket 		  = UDPPacket()
						extracted_data    = recvPacket.disassemble(packet[1],self.skipper)
						if extracted_data != None:
							if 'close' in extracted_data:
								closed_port.put(extracted_data)
								self.counter.StartCount(1)
							else:
								open_port.put(extracted_data)
								self.counter.StartCount(17)
						else:
							pass

		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))


class ActiveUdpScan:
	def __init__(self,tgt,prange,to):
		self.tgt    = tgt
		self.prange = confirm_port_range(prange)
		self.to 	= float(to)
		self.mysock = create_udp_socket(self.to)
		self.single = False

	def _get_dip(self):
		return resolve_host(self.tgt)

	def _start(self):
		t1=time.time()

		if len(self.prange) == 1:
			self.single = True
			for num in self.prange:
				port = num
		else:
			srange        = int(self.prange[0])
			erange        = int(self.prange[1])+1

		sip 	      = get_our_addr()
		dip 	      = self._get_dip()

		sport 	      = randrange(1,65535)

		setup_catcher = Catch_packet(dip)
		catcher       = setup_catcher._set_udp()
		counter 	  = CountPort()
		skipper 	  = SkipPort()

		data 		  = '\x00' * 20

		s 			  = Semaphore(1000)
		locker 		  = RLock()

		threads 	  = []
		open_ports 	  = []
		closed_ports  = []
		OFP_ports 	  = []

		field         = ['Port','Serv','TTL','State','Reason']
		mytable 	  = PrettyTable(field)

		if self.single == True:
			setup_packet = UDPPacket(data,int(port),sport,dip,sip)
			packet 		 = setup_packet.assemble()
			pool  	     = UdpScanner(self.mysock,
                                       dip,
                                       int(port),
                                       packet,
                                       catcher,
                                       locker,
                                       counter,
                                       skipper,
                                       self.single)
			t 		     = Thread(target=start_pool,args=(s,pool))
			t.daemon	 = True
			t.start()
			t.join()

		else:
			try:
				for dport in xrange(srange,erange):
					setup_packet = UDPPacket(data,dport,sport,dip,sip)
					packet       = setup_packet.assemble()
					pool 		 = UdpScanner(self.mysock,
                                              dip,
                                              dport,
                                              packet,
                                              catcher,
                                              locker,
                                              counter,
                                              skipper,
                                              self.single)
					t 			= Thread(target=start_pool,args=(s,pool))
					threads.append(t)

				for thread in threads:
					thread.daemon=True
					thread.start()

				for thread in threads:
					thread.join()

			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user','red'))


		while 1:
			if not closed_port.empty():
				cp=closed_port.get()
				if cp != None:
						closed_ports.append(cp)
			else:
				break

		while 1:
			if not open_port.empty():
				op=open_port.get()
				if op != None:
					open_ports.append(op)
			else:
				break

		while 1:
			if not OFP.empty():
				ofp=OFP.get()
				if ofp != None:
					OFP_ports.append(ofp)
			else:
				break
		(open_ps,closed_ps,ofps) = counter.Result()

		if self.single == False:

			if open_ps < closed_ps and open_ps < ofps:
				if closed_ps < ofps and closed_ps > 0:
					
					total_data = open_ports + closed_ports
					for data in total_data:
						mytable.add_row(data)
					print mytable
					of_len = len(OFP_ports) - 1
					print 'Got {} ports open|filtered'.format(colored(of_len,'red'))

				elif closed_ps > ofps and ofps > 0:
					total_data = open_ps + OFP_ports
					for data in total_data:
						mytable.add_row(data)
					print mytable
					cl_len = len(closed_ports) - 1
					print 'Got {} ports closed'.format(colored(cl_len,'red'))

			elif closed_ports < open_ports and closed_ports < ofps:
				if ofps < open_ports and ofps > 0:
					total_data = closed_ports + OFP_ports
					for data in total_data:
						mytable.add_row(data)
					print mytable
					op_len = len(open_ports) - 1
					print 'Got {} ports open'.format(colored(op_len,'red'))

			elif ofps == (erange - srange):
				of_len = len(OFP_ports) - 1
				print 'Got {} ports open|filtered'.format(colored(of_len,'red'))

			elif closed_ports == (erange - srange):
				cl_len = len(closed_ports) - 1
				print 'Got {} ports closed'.format(colored(cl_len,'red'))

			elif open_ports == (erange - srange):
				op_len = len(open_ports) - 1
				print 'Got {} ports open'.format(colored(op_len,'red'))
		else:
			if open_ps > closed_ps and open_ps > ofps:
				for data in open_ports:
					mytable.add_row(data)
				print mytable
			elif closed_ports > open_ports and closed_ports > ofps:
				for data in closed_ports:
					mytable.add_row(data)
				print mytable
			elif ofps > open_ps and ofps > closed_ps:
				for data in OFP_ports:
					mytable.add_row(data)
				print mytable

		t2=time.time()
		tt=t2-t1

		print 'Collector finished scan in '+colored(tt,'yellow')+' sec'

