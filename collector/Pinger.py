import os
import sys
import time
import struct
from socket import *
from termcolor import colored,cprint
from Traceroute.MyPacket import *
sys.dont_write_bytecode=True

class IPPinger:
    def __init__(self,ip,sr,er):
        self.ip       = ip
        self.sr       = sr
        self.er       = er
        self.type     = 8
        self.code     = 0
        self.cksum    = 0
        self.toip     = []
        self.mypacket = ''
        self.id       = os.getpid() & 0xFFFF

    def create_ips(self):
        ipaddrs=[]
        ip=self.ip.split('.')
        delElement=ip.pop(3)
        mystr='.'.join(ip)
        for x in xrange(self.sr,self.er):
            ipaddr=mystr+'.'+str(x)
            ipaddrs.append(ipaddr)
        return ipaddrs

    def checksum(self,data):
        csum = 0
        countTo = (len(data) / 2) * 2
        count = 0
        while count < countTo:
            thisVal = ord(data[count+1]) * 256 + ord(data[count])
            csum = csum + thisVal
            csum = csum & 0xffffffffL
            count = count + 2
        if countTo < len(data):
            csum = csum + ord(data[len(data) - 1])
            csum = csum & 0xffffffffL
        csum = (csum >> 16) + (csum & 0xffff)
        csum = csum + (csum >> 16)
        answer = ~csum
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer

    def building_packet(self):
        header=struct.pack('bbHHh',self.type,self.code,self.cksum,self.id,1)
        data=struct.pack('d',time.time())
        mycksum=self.checksum(header+data)
        if sys.platform == 'darwin':
            mycksum=htons(mycksum) & 0xffff
        else:
            mycksum=htons(mycksum)
        header=struct.pack('bbHHh',self.type,self.code,mycksum,self.id,1)
        packet=header+data
        return packet

    def building_socket(self):
        try:
            sock=socket(AF_INET,SOCK_RAW,IPPROTO_ICMP)
        except Exception:
            raise Exception(e)
        return sock
    def get_status(self,pkt):
        try:
            icmpstatus=icmphdr.disassemble(pkt[20:28])
            if (icmpstatus.type == 8 and icmpstatus.code == 0):
                return 'Alive'
            elif (icmpstatus.type == 0 and icmpstatus.code == 0):
                return 'Alive'
            else:
                return 'Dead'
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))

    def ping_process(self):
        ips=self.create_ips()
        pkt=self.building_packet()
        mysock=self.building_socket()
        mysock.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
        mysock.settimeout(0.05)
        for ip in ips:
            self.ping(ip,mysock,pkt)
        for ip in self.toip:
            self.reping(ip,mysock,pkt)

    def ping(self,ip,mysock,pkt):
        try:
            mysock.sendto(pkt,(ip,0))
            d,addr=mysock.recvfrom(4096)
            status=self.get_status(d)
            if status == 'Alive':
                print colored(ip,'green')
            if status == 'Dead':
                print colored('ICMP Host Unreachable from ','red')+colored(addr[0],'red')+colored(' for ICMP Echo sent to ','red')+colored(ip,'red')
        except Exception:
            self.toip.append(ip)
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))

    def reping(self,ip,mysock,pkt):
        try:
            mysock.settimeout(3)
            mysock.sendto(pkt,(ip,0))
            d,addr=mysock.recvfrom(4096)
            status=self.get_status(d)
            if status == 'Alive':
                print colored(ip,'green')
            if status == 'Dead':
                print colored('ICMP Host Unreachable from ','red')+colored(addr[0],'red')+colored(' for ICMP Echo sent to ','red')+colored(ip,'red')
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))