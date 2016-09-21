import sys
import pcap
from socket import *
from termcolor import cprint,colored
sys.dont_write_bytecode=True

def resolve_host(tgt):
	return gethostbyname(tgt)

def convert_int(num):
	return htons(num)

def getportserv(port):
	try:
		s = str(getservbyport(port))
	except:
		s = ("unknown")
	return s

def get_our_addr():
	s=socket(AF_INET,SOCK_DGRAM)
	s.connect(('google.com',0))
	return s.getsockname()[0]

def convert_ip(sip,dip):
	saddr=inet_aton(sip)
	daddr=inet_aton(dip)
	return (saddr,daddr)

def create_tcp_socket(to,type):
	if type == 'conn':
		mysock=socket(AF_INET,SOCK_STREAM)
		mysock.settimeout(to)
	else:
		try:
			mysock=socket(AF_INET,SOCK_RAW,IPPROTO_TCP)
			mysock.setsockopt(IPPROTO_IP,IP_HDRINCL,1)
			mysock.settimeout(to)
		except Exception,e:
			raise Exception(e)
			sys.exit(1)

	return mysock

def create_udp_socket(to):
	try:
		mysock=socket(AF_INET,SOCK_RAW,IPPROTO_UDP)
		mysock.settimeout(to)
	except Exception,e:
		raise Exception(e)
		sys.exit(1)
	return mysock

class Catch_packet:
	def __init__(self,tgt):
		self.tgt=tgt
		self.dev=pcap.lookupdev()

	def _set_tcp(self):
		p = pcap.pcapObject()
		p.open_live(self.dev, 99999, 0, 100)
		p.setfilter(('src host ') + str(self.tgt),0,0)
		return p

	def _set_udp(self):
		p = pcap.pcapObject()
		p.open_live(self.dev, 99999, False, 1)
		p.setfilter('src host ' + str(self.tgt),0,0)
		return p