import sys
from socket import *
from MyPacket import *
sys.dont_write_bytecode=True

class Builder(object):
    def __init__(self, target, ttl, proto, dport=None, sport=None):
        self.proto = proto
        self.dport = dport
        self.sport = sport

        self.found = False
        self.tries = 0
        self.last_try = 0
        self.remote_ip = None
        self.remote_icmp = None
        self.remote_host = None
        self.location = ""

        self.ttl = ttl
        self.ip = iphdr(dst=target)
        self.ip.ttl = ttl
        self.ip.id += ttl
        if self.proto == "icmp":
            self.icmp = icmphdr('\x00' * 20)
            self.icmp.id = self.ip.id
            self.ip.data = self.icmp.assemble()

        self._pkt = self.ip.assemble()

    @property
    def pkt(self):
        return self._pkt