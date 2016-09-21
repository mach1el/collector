import sys
import json
import time
import select
import requests
from random import *
from Builder import *
from termcolor import colored,cprint
sys.dont_write_bytecode=True

class Traceroute:
    def __init__(self,tgt,hops):
        self.tgt    = gethostbyname(tgt)
        self.hops   = hops
        self.to     = 2.0
        self.recvto = pack('ll',2,0)

    def resolver(self,addrs):
        try:
            host=gethostbyaddr(addrs)
            mystr='{0} :: {1}'.format(addrs,host[0])
        except:
            mystr='{0} :: {0}'.format(addrs)
        return mystr

    def geoip(self,ip):
        try:
            r=requests.get('http://freegeoip.net/json/'+ip)
            rs=r.content
            d=json.loads(rs)
            items=[d['country_name'],d['region_name'],d['city']]
            if items == None:
                return
            else:
                result=', '.join([x for x in items if x])
                return result.encode('utf-8')
        except Exception,e:
            cprint(e,'red')
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))

    def _start_icmp(self):
        for ttl in xrange(1,(self.hops+1)):
            recver=socket(AF_INET,SOCK_RAW,IPPROTO_ICMP)
            sender=socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
            sender.setsockopt(SOL_IP,IP_TTL,pack('I',ttl))
            recver.bind(("",0))

            try:
                build_packet = Builder(self.tgt,ttl,'icmp')
                pkt 		 = build_packet.pkt

                port = randrange(33434,33460)
                sender.sendto(pkt,(self.tgt,port))

                t       = time.time()
                started = time.time()
                ready   = select.select([recver],[],[],self.to)
                hmt 	= (time.time()-started)

                if ready[0]==[]:
                    sys.stdout.write('* ')
                    continue
                recvPkt,addrs=recver.recvfrom(65565)
                timerecv=time.time()
            except timeout:
                pass
            except KeyboardInterrupt:
                sys.exit(cprint('[-] Canceled by user','red'))
            else:
                geoip=self.geoip(addrs[0])
                print_result=self.resolver(addrs[0])
                print '%d %.2fms %s :: %s' % (ttl,(timerecv-started),print_result,geoip)
            finally:
            	sys.stdout.flush()
                recver.close()
                sender.close()
