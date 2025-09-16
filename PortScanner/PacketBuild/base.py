# -*- coding: utf-8 -*-

import sys
import socket
import struct
from random import randrange

def get_system_ttl():
  """Guess typical TTL based on OS."""
  plat = sys.platform
  if 'linux' in plat:
    return 64
  if 'win' in plat:
    return 128
  return 255

# TCP flag bitmasks
TCP_FLAGS = {
    'fin': 0x01,
    'syn': 0x02,
    'rst': 0x04,
    'psh': 0x08,
    'ack': 0x10,
    'urg': 0x20,
    'xmas': 0x29,
    'null': 0x00,
}

class SocketHandler:
  """Encapsulates socket creation for raw scans and ICMP receive."""
  def __init__(self, timeout=1.0):
    self.timeout = timeout

  def connect_socket(self, addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(self.timeout)
    try:
      s.connect((addr, port))
      return s
    except:
      s.close()
      return None

  def raw_socket(self, proto):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto)
    s.settimeout(self.timeout)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    return s

  def icmp_socket(self):
    # Listen for ICMP unreachable for UDP scans
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.settimeout(self.timeout)
    return s

class PacketBuilder:
  """Builds IP/TCP/UDP packets with checksums."""
  def __init__(self, src_ip, dst_ip):
    self.src_ip = src_ip
    self.dst_ip = dst_ip

  def checksum(self, data):
    if len(data) % 2:
      data += b'\x00'
    s = sum(struct.unpack('!%dH' % (len(data)//2), data))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return ~s & 0xffff

  def build_ip_header(self, payload_len, proto):
    version_ihl = (4 << 4) + 5
    tos = 0
    tot_len = 20 + payload_len
    packet_id = randrange(0, 65535)
    flags_frag = 0
    ttl = get_system_ttl()
    checksum = 0
    src = socket.inet_aton(self.src_ip)
    dst = socket.inet_aton(self.dst_ip)
    return struct.pack('!BBHHHBBH4s4s', version_ihl, tos, tot_len,
                        packet_id, flags_frag, ttl, proto,
                        checksum, src, dst)

  def build_tcp_header(self, src_port, dst_port, flags):
    seq = randrange(0, 0xFFFF_FFFF)
    ack_seq = 0
    offset_res = (5 << 4)
    window = socket.htons(5840)
    urg_ptr = 0
    # initial header without checksum
    hdr = struct.pack('!HHLLBBHHH', src_port, dst_port,
                      seq, ack_seq, offset_res,
                      flags, window, 0, urg_ptr)
    # pseudo-header
    pseudo = struct.pack('!4s4sBBH',
                          socket.inet_aton(self.src_ip),
                          socket.inet_aton(self.dst_ip),
                          0, socket.IPPROTO_TCP,
                          len(hdr))
    chksum = self.checksum(pseudo + hdr)
    # rebuild with checksum
    return struct.pack('!HHLLBBH', src_port, dst_port,
                        seq, ack_seq, offset_res,
                        flags, window) + struct.pack('H', chksum) + struct.pack('!H', urg_ptr)

  def build_udp_header(self, src_port, dst_port, payload=b''):
    length = 8 + len(payload)
    hdr = struct.pack('!HHHH', src_port, dst_port, length, 0)
    pseudo = struct.pack('!4s4sBBH',
                          socket.inet_aton(self.src_ip),
                          socket.inet_aton(self.dst_ip),
                          0, socket.IPPROTO_UDP,
                          length)
    chksum = self.checksum(pseudo + hdr + payload)
    return struct.pack('!HHH', src_port, dst_port, length) + struct.pack('H', chksum)

class CatchPacket:
  """Simplified packet sniffer for TCP and ICMP responses."""
  def __init__(self, iface_ip):
    self.iface = iface_ip
    self.sock = None

  def _set_tcp(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    self.sock.settimeout(1.0)
    return self

  def _set_icmp(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    self.sock.settimeout(1.0)
    return self

  def next(self):
    try:
      pkt, addr = self.sock.recvfrom(65535)
      return pkt, addr
    except socket.timeout:
        return None

  def get_service(self, port):
    try:
      return socket.getservbyport(port)
    except:
      return ''