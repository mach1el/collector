import sys
import time
from threading import *
from Queue import Queue
from prettytable import PrettyTable
from termcolor import colored,cprint
from myhandler.socket_handler import *
sys.dont_write_bytecode=True

p=Queue()

def start_pool(s,pool):
	with s:
		pool._TCP_multiple()

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

class Scanner(object):
	def __init__(self,
		        tgt,
		        port,
		        to,
		        lock,
		        quite):
		super(Scanner,self).__init__()
		self.tgt 	= tgt
		self.port   = port
		self.to 	= to
		self.lock   = lock
		self.quite 	= quite
		self.c 		= 0

	def _TCP_multiple(self):
		try:
			mysock = create_tcp_socket(self.to,'conn')
			try:
				with self.lock:
					self.c+=1
					d=mysock.connect_ex((self.tgt,self.port))
				if d == 0:
					with self.lock:
						self.c+=1
						serv = getportserv(self.port)
						if self.quite == True:
							data=(str(self.port),'open',serv)
							p.put(data)
						else:
							print str(self.port).ljust(7)+'open'.ljust(7)+serv

			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user','red'))
			finally:
				pass

		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))
		except:
			pass
		finally:
			pass

	def _TCP_single(self):
		try:
			mysock = create_tcp_socket(self.to,'conn')
			mysock.connect((self.tgt,int(self.port)))
			mysock.send('')
			mysock.close()
			serv = getportserv(int(self.port))
			print str(self.port).ljust(7)+'open'.ljust(7)+serv
		except timeout:
			print '[-] Timed out'
		except error:
			print str(self.port).ljust(7)+'closed'.ljust(7)+getportserv(int(self.port))
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))

class ActiveThreads(object):
	def __init__(self,tgt,to,prange,quite):
		self.tgt 	= gethostbyname(tgt)
		self.to 	= float(to)
		self.prange = confirm_port_range(prange)
		self.quite  = quite
		self.single = False

	def _start(self):

		start   = time.clock()

		if len(self.prange) == 1:
			self.single = True
			for num in self.prange:
				port = num
		else:
			srange  = int(self.prange[0])
			erange  = int(self.prange[1])+1

		s 	    = Semaphore(1000)
		lock 	= Semaphore(10000)
		threads = []
		datas   = []

		table   = PrettyTable(['PORT','STATE','SERVICE'])

		if self.single == True:
			pool = Scanner(self.tgt,
                           port,
                           self.to,
                           lock,
                           self.quite)
			pool._TCP_single()
		else:
			try:
				for port in xrange(srange,erange):
					pool = Scanner(self.tgt,
                                   port,
                                   self.to,
                                   lock,
                                   self.quite)
					t 	 = Thread(target=start_pool,args=(s,pool))
					threads.append(t)

				for thread in threads:
					thread.daemon=True
					thread.start()

				for x in xrange(len(threads)):
					threads[x].join()

			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user','red'))

		if self.quite == True:
			while 1:
				if not p.empty():
					data = p.get()
					if data != None:
						datas.append(data)
				else:
					break
			for data in datas:
				table.add_row(data)
			print table

		end=time.clock()

		total_time=end-start
		print colored('\nCollector finished scan in:','blue')+colored(' {} '.format(total_time),'yellow')+colored('sec','blue')

