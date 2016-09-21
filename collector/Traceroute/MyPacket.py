import os
import sys
import operator
from random import *
from struct import *
from socket import *
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


class iphdr(object):
    def __init__(self, proto=IPPROTO_ICMP, src="0.0.0.0", dst=None,id=None):
        self.version = 4
        self.hlen    = 5
        self.tos     = 0
        self.length  = 20
        self.id = id
        if self.id == None:
            self.id = os.getpid() & 0xFFFF
        self.frag    = 0
        self.ttl     = 255
        self.proto   = proto
        self.cksum   = 0
        self.src     = src
        self.saddr   = inet_aton(src)
        self.dst     = dst or "0.0.0.0"
        self.daddr   = inet_aton(self.dst)
        self.data    = ""

    def assemble(self):
        header = pack('BBHHHBB',
                             (self.version & 0x0f) << 4 | (self.hlen & 0x0f),
                             self.tos, self.length + len(self.data),
                             htons(self.id), self.frag,
                             self.ttl, self.proto)
        self._raw = header + "\x00\x00" + self.saddr + self.daddr + self.data
        return self._raw

    @classmethod
    def disassemble(self, data):
        self._raw  = data
        ip         = iphdr(IPPROTO_TCP)
        pkt        = unpack('!BBHHHBBH', data[:12])
        ip.version = (pkt[0] >> 4 & 0x0f)
        ip.hlen    = (pkt[0] & 0x0f)
        ip.tos, ip.length, ip.id, ip.frag, ip.ttl, ip.proto, ip.cksum = pkt[1:]
        ip.saddr   = data[12:16]
        ip.daddr   = data[16:20]
        ip.src     = inet_ntoa(ip.saddr)
        ip.dst     = inet_ntoa(ip.daddr)
        return ip

    def __repr__(self):
        return "IP (tos %s, ttl %s, id %s, frag %s, proto %s, length %s) " \
               "%s -> %s" % \
               (self.tos, self.ttl, self.id, self.frag, self.proto,
                self.length, self.src, self.dst)

class icmphdr(object):
    def __init__(self, data=""):
        self.type     = 8
        self.code     = 0
        self.cksum    = 0
        self.id       = randint(2**10,2**16)
        self.sequence = 0
        self.data     = data

    def assemble(self):
        part1 = pack("BB", self.type, self.code)
        part2 = pack("!HH", self.id, self.sequence)
        cksum = self.checksum(part1 + "\x00\x00" + part2 + self.data)
        cksum = pack("!H", cksum)
        self._raw = part1 + cksum + part2 + self.data
        return self._raw

    @classmethod
    def checksum(self, data):
        if len(data) & 1:
            data += "\x00"
        cksum = reduce(operator.add,
                       unpack('!%dH' % (len(data) >> 1), data))
        cksum = (cksum >> 16) + (cksum & 0xffff)
        cksum += (cksum >> 16)
        cksum = (cksum & 0xffff) ^ 0xffff
        return cksum

    @classmethod
    def disassemble(self, data):
        self._raw = data
        icmp = icmphdr()
        pkt = unpack("!BBHHH", data)
        icmp.type, icmp.code, icmp.cksum, icmp.id, icmp.sequence = pkt
        return icmp

    def __repr__(self):
        return "ICMP (type %s, code %s, id %s, sequence %s)" % \
               (self.type, self.code, self.id, self.sequence)
