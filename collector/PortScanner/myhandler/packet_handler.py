import sys
import array
from random import *
from struct import *
from threading import *
from socket_handler import *
sys.dont_write_bytecode=True


def macth_ttl():
  if sys.platform == 'linux2':
	return 64
  elif sys.platform == 'win32':
	return 128
  else:
	return 255

def macth_winz():
	if sys.platform == 'linux2':
		return 5840
	elif sys.platform == 'win32':
		return 8192
	else:
		return 4128

def macth_flag(type):
	if type == 'fin':
	  tcp_fin	 = 1
	  tcp_syn	 = 0
	  tcp_rst	 = 0
	  tcp_psh	 = 0
	  tcp_ack	 = 0
	  tcp_urg	 = 0
	  return (tcp_fin,tcp_syn,tcp_rst,tcp_psh,tcp_ack,tcp_urg)

	elif type == 'syn':
	  tcp_fin	 = 0
	  tcp_syn	 = 1
	  tcp_rst	 = 0
	  tcp_psh	 = 0
	  tcp_ack	 = 0
	  tcp_urg	 = 0
	  return (tcp_fin,tcp_syn,tcp_rst,tcp_psh,tcp_ack,tcp_urg)

	elif type == 'ack':
	  tcp_fin	 = 0
	  tcp_syn	 = 0
	  tcp_rst	 = 0
	  tcp_psh	 = 0 
	  tcp_ack	 = 1
	  tcp_urg	 = 0
	  return (tcp_fin,tcp_syn,tcp_rst,tcp_psh,tcp_ack,tcp_urg)

	elif type == 'xmas':
	  tcp_fin	 = 1
	  tcp_syn	 = 0
	  tcp_rst	 = 0 
	  tcp_psh	 = 1
	  tcp_ack	 = 0 
	  tcp_urg	 = 1
	  return (tcp_fin,tcp_syn,tcp_rst,tcp_psh,tcp_ack,tcp_urg)
	  
	elif type == 'null':
	  tcp_fin	 = 0
	  tcp_syn	 = 0
	  tcp_rst	 = 0 
	  tcp_psh	 = 0
	  tcp_ack	 = 0 
	  tcp_urg	 = 0
	  return (tcp_fin,tcp_syn,tcp_rst,tcp_psh,tcp_ack,tcp_urg)


class UnpackPacket:
	def __init__(self,packet,quite,PortSkipper):
		self.packet	  = packet
		self.quite	   = quite
		self.skip_port   = []
		self.PortSkipper = PortSkipper
		self.reason	  = 'syn-ack'
		self.state	   = 'open'

	def _unpackTCP(self):
		data = self.packet[14:]
		ttl=ord(data[8])
		header_len = ord(data[0]) & 0x0f
		data = data[4*header_len:]
		(tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr) = unpack('!HHLLBBHHH', data[:20])
		if tcp_source:
			port=self.PortSkipper._skip(tcp_source)
			if port == None:
				pass
			else:
				serv=getportserv(port)
				if self.quite == None:
				  return (str(port),self.state,serv)
				if self.quite == True:
					return (str(port),serv,tcp_window,ttl,self.reason)
				else:
					return (port,serv,self.state)

	def _unpackAckScan(self):
	  packet	   = self.packet[0]
	  eth_length   = 14
	  eth_header   = packet[:eth_length]
	  eth		  = unpack('!6s6sH' , eth_header)
	  eth_protocol = socket.ntohs(eth[2])

	  if eth_protocol == 8 :
		ip_header   = self.packet[eth_length:20+eth_length]
		iph		 = unpack('!BBHHHBBH4s4s' , ip_header)
		version_ihl = iph[0]
		version	 = version_ihl >> 4
		ihl		 = version_ihl & 0xF
		iph_length  = ihl * 4
		ttl		 = iph[5]
		protocol	= iph[6]
		s_addr	  = socket.inet_ntoa(iph[8]);
		d_addr	  = socket.inet_ntoa(iph[9]);

		if protocol == 6 :
		  t			   = iph_length + eth_length
		  tcp_header	  = self.packet[t:t+20]
		  tcph			= unpack('!HHLLBBHHH' , tcp_header)   
		  source_port	 = tcph[0]
		  dest_port	   = tcph[1]
		  sequence		= tcph[2]
		  acknowledgement = tcph[3]
		  doff_reserved   = tcph[4]
		  tcph_length	 = doff_reserved >> 4

		  if source_port:
			serv = getportserv(source_port)
			return (str(port),'filtered',serv)

		elif protocol == 1 :
		  u			= iph_length + eth_length
		  icmph_length = 4
		  icmp_header  = self.packet[u:u+4]
		  icmph		= unpack('!BBH' , icmp_header)
		  icmp_type	= icmph[0]
		  code		 = icmph[1]
		  checksum	 = icmph[2]

		  h_size	   = eth_length + iph_length + icmph_length
		  mydata	   = data[h_size+4:]

		  extracted_data = unpack('!HH',mydata[20:24])
		  (dport,sport)  = extracted_data
		  if sport:
			serv = getportserv(sport)
			if code:
			  r	  = UDPPacket()
			  reason = r._UDPPacket__match_code_reason(code)
			  return (str(port),'filtered',serv,reason)

class TCPPacket:
	def __init__(self,  
				tgt,
				dport,
				ouraddr,
				type):
		self.tgt	 = tgt
		self.dport   = dport
		self.ouraddr = ouraddr
		self.type	= type

	def cksum(self,packet):
		s=0
		for i in range(0,len(packet),2):
			w=(ord(packet[i]) << 8) + (ord(packet[i+1]))
			s=s+w
		s=(s>>16)+(s&0xffff);
		s=s+(s>>16);
		s=~s&0xffff
		return s

	def building_packet(self):

		ip_ihl	  = 5 
		ip_ver	  = 4
		ip_tos	  = 0 
		ip_tot_len  = 20+20
		ip_id	   = 54321
		ip_frag_off = (1 << 1) << 13
		ip_ttl	  = macth_ttl()
		ip_proto	= IPPROTO_TCP 
		ip_check	= 0
		myip		= convert_ip(self.ouraddr,self.tgt)
		ip_saddr	= myip[0]
		ip_daddr	= myip[1]

		ip_ihl_ver  = (ip_ver << 4) + ip_ihl

		ip_header   = pack('!BBHHHBBH4s4s', 
						   ip_ihl_ver, 
						   ip_tos, 
						   ip_tot_len, 
						   ip_id, 
						   ip_frag_off, 
						   ip_ttl, 
						   ip_proto, 
						   ip_check,
						   ip_saddr, 
						   ip_daddr)

		tcp_source  = randrange(1024,65535)
		tcp_dest	= (self.dport)
		tcp_seq	 = 123456
		tcp_ack_seq = 0
		tcp_doff	= 6

		(tcp_fin,tcp_syn,tcp_rst,tcp_psh,tcp_ack,tcp_urg) = macth_flag(self.type)

		tcp_window  = convert_int(macth_winz())
		tcp_check   = 0 
		tcp_urg_ptr = 0


		tcp_offset_res = (tcp_doff << 4) 
		tcp_flags	  = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)

		options		= (2 << 24) | (4 << 16) | (1460 << 0)

		tcp_header	 = pack('!HHLLBBHHHL', 
							   tcp_source, 
							   tcp_dest, 
							   tcp_seq, 
							   tcp_ack_seq, 
							   tcp_offset_res, 
							   tcp_flags, 
							   tcp_window, 
							   tcp_check, 
							   tcp_urg_ptr,
							   options)

		user_data	  = ''
		tcp_length	 = len(tcp_header + user_data)

		psh			= pack('!4s4sBBH', 
							   ip_saddr, 
							   ip_daddr, 
							   0, 
							   ip_proto, 
							   tcp_length);
		psh			= psh + tcp_header;

		tcp_check	  = self.cksum(psh)
		tcp_header	 = pack('!HHLLBBHHHL', 
							   tcp_source, 
							   tcp_dest, 
							   tcp_seq, 
							   tcp_ack_seq, 
							   tcp_offset_res, 
							   tcp_flags, 
							   tcp_window, 
							   tcp_check, 
							   tcp_urg_ptr,
							   options)

		return  (ip_header + tcp_header + user_data)

class UDPPacket(object):
	def __init__(self,data="",dport=4242,sport=4242,ouraddr=None,tgt=None):
	  self.data	= data
	  self.dport   = dport
	  self.sport   = sport
	  self.ouraddr = ouraddr
	  self.tgt	 = tgt
	  self.cksum   = 0
	  self.length  = len(self.data) + 8

	def assemble(self):
	  part1	  = inet_aton(self.ouraddr) +\
				   inet_aton(self.tgt)	  +\
				   pack('!BBH',
						 0,
						 IPPROTO_UDP,
						 self.length)
	  udp_header = pack('!HHHH',
						 self.sport,
						 self.dport,
						 self.length,
						 0)
	  cksum	  = self.checksum(part1 + udp_header)

	  packet	 = pack('!HHHH',
						 self.sport,
						 self.dport,
						 self.length,
						 cksum) +\
				   self.data

	  return packet

	@classmethod
	def checksum(self,data):
	  if pack('H',1) == '\x00\x01':
		if len(data) % 2 == 1:
		  data += '\0'
		s=sum(array.array('H',data))
		s=(s >> 16) + (s & 0xffff)
		s+=s >> 16
		s=~s
		return s & 0xffff
	  else:
		if len(data) % 2 == 1:
		  data += '\0'
		s=sum(array.array('H',data))
		s=(s >> 16) + (s & 0xffff)
		s+=s >> 16
		s=~s
		return (((s >> 8)&0xff)|s << 8) & 0xffff

	def disassemble(self,data,skipper):
	  eth_length   = 14
	  eth_header   = data[:eth_length]
	  eth		  = unpack('!6s6sH' , eth_header)
	  eth_protocol = ntohs(eth[2])
	  if eth_protocol == 8 :
		ip_header   = data[eth_length:20+eth_length]
		iph		 = unpack('!BBHHHBBH4s4s' , ip_header)
		version_ihl = iph[0]
		version	 = version_ihl >> 4
		ihl		 = version_ihl & 0xF
		iph_length  = ihl * 4
		ttl		 = iph[5]
		protocol	= iph[6]
		s_addr	  = inet_ntoa(iph[8]);
		d_addr	  = inet_ntoa(iph[9]);

		if protocol == 1:
		  u			= iph_length + eth_length
		  icmph_length = 4
		  icmp_header  = data[u:u+4]
		  icmph		= unpack('!BBH' , icmp_header)
		  type		 = icmph[0]
		  code		 = icmph[1]
		  checksum	 = icmph[2]
		  h_size	   = eth_length + iph_length + icmph_length
		  mydata	   = data[h_size+4:]

		  extracted_data = unpack('!HH',mydata[20:24])
		  (dport,sport)  = extracted_data
		  if sport:
			port = skipper._skip(sport)
			if port == None:
			  pass
			else:
			  serv = getportserv(sport)
			  if code:
				r	  = UDPPacket()
				reason = r._UDPPacket__match_code_reason(code)
				return (port,serv,ttl,'close',reason)

		  elif protocol == 17:
			u			= iph_length + eth_length
			udph_length  = 8
			udp_header   = data[u:u+8]
			udph		 = unpack('!HHHH' , udp_header)
			source_port  = udph[0]
			dest_port	= udph[1]
			length	   = udph[2]
			checksum	 = udph[3]

			if source_port:
			  port = skipper._skip(source_port)
			  if port == None:
				pass
			  else:
				serv = getportserv(source_port)
				if code:
				  return (sport,serv,ttl,'close','udp-response')

	def __match_code_reason(self,code):
	  if code == 0:
		return 'Net unreachable'
	  elif code == 1:
		return 'Host unreachable'
	  elif code == 2:
		return 'Protocol unreachable'
	  elif code == 3:
		return 'Port unreachable'
	  elif code == 4:
		return 'Fragmentation needed and Don\'t fragment was set'
	  elif code == 5:
		return 'Source route failed'
	  elif code == 6:
		return 'Destination network unknown'
	  elif code == 7:
		return 'Destination host isolated'
	  elif code == 9:
		return 'Network prohibited'
	  elif code == 10:
		return 'Host prohibited'
	  elif code == 11:
		return 'DST network unreachable for type of service'
	  elif code == 12:
		return 'DST host unreachable for type of service'
	  elif code == 13:
		return 'Communication Administratively Prohibited'
	  elif code == 14:
		return 'Host Precedence Violation'
	  elif code == 15:
		return 'Precedence cutoff in effect'
