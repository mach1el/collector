import sys
from socket import *
from dns import rdata
from dns import zone
from dns import query
from dns import resolver
from dns import reversename
from termcolor import colored,cprint
sys.dont_write_bytecode=True


class Convert_address(object):
    def __init__(self,ip4=None):
        self.ip4       = ip4
        self.ip6       = ip6
        self.ip4_str   = 'in-addr.arpa'
        self.ip4_addr  = ''
        self._converting()

    def _converting(self):
        ip4_str       = self.ip4.split('.')
        ip4_addr      = '{}.{}.{}.{}'.format(ip4_str[2],
                                             ip4_str[1],
                                             ip4_str[0],
                                             self.ip4_str)
        self.ip4_addr = ip4_addr

    def _return_my_addr(self):
        return (self.ip4_addr)

class lookup_dns:
    def __init__(self,d):
        self.d              = d
        self.types          = [
            "A","AAAA","AFSDB","APL","CAA","CDNSKEY","CDS","CERT","CNAME","DHCID",
            "DLV","DNAME","DNSKEY","DS","HIP","IPSECKEY","KEY","KX","LOC","MX","NAPTR",
            "NS","NSEC","NSEC3","NSEC3PARAM","PTR","RRSIG","RP","SIG","SOA","SRB","SSHFP",
            "TA","TKEY","TLSA","TSIG","TXT","*","AXFR","IXFR","OPT","SRV","HINFO"
        ]
        self.name           = ''
        self.ip6            = ''

    def resolve_PTR(self):
        try:
            addr = reversename.from_address(self.d)
            data = str(resolver.query(addr,'PTR')[0])
            return data
        except:
            pass

    def some(self):
        self.ip = gethostbyname(self.d)

        try:
            name      = reversename.from_address(self.ip)
            self.name = str(name).rstrip('.')
        except:
            self.name = self.ip

        print colored('Name: ','blue') + colored(self.name,'green')
        print colored('IP Address: ','blue') + colored(self.ip,'green')

    def look_up(self):
        print colored('[*] DNS record for: {}'.format(colored(self.d,'green')),'blue')
        for type in self.types:
            try:
                ans = resolver.query(self.d,type)
                for rdata in ans:
                    if type == 'AAAA':
                        try:
                            self.ip6 = rdata
                        except:
                            pass
                    if type == 'MX':
                        ex  = colored(str(rdata.exchange).rstrip('.'),'green')
                        pre = colored(rdata.preference,'green')
                        print '[+]  {}'.format(colored(type,'blue'))
                        print ('\t _exchange: {0}\n'
                               '\t|__Preference: {1}').format(ex,pre)

                    elif type == 'SOA':
                        
                        server  = colored(str(rdata.mname).rstrip('.'),'green')
                        rname   = colored(str(rdata.rname).rstrip('.'),'green')
                        serial  = colored(rdata.serial,'green')
                        refresh = colored(rdata.refresh,'green')
                        retry   = colored(rdata.retry,'green')
                        expire  = colored(rdata.expire,'green')
                        minimum = colored(rdata.minimum,'green')

                        print '[+]  {}'.format(colored(type,'blue'))
                        print ('\t _server: {0}'
                               '\n\t|__email: {1}'
                               '\n\t|___serial: {2}'
                               '\n\t|____refresh: {3}'
                               '\n\t|_____retry: {4}'
                               '\n\t|______expire: {5}'
                               '\n\t|_______minimum ttl: {6}').format(server,rname,serial,refresh,retry,expire,minimum)
                    else:
                        print '[+]  {0} {1}'.format(colored(type,'blue'),colored(str(rdata).rstrip('.'),'green'))
            except Exception:
                pass
            except KeyboardInterrupt:
                sys.exit(cprint('[-] Canceled by user','red'))

        print colored('\n[*] DNS record for: {}'.format(colored(self.name,'green')),'blue')
        for type in self.types:
            try:
                ans = resolver.query(self.name,type)
                for rdata in ans:
                    if type == 'MX':
                        ex  = colored(str(rdata.exchange).rstrip('.'),'green')
                        pre = colored(rdata.preference,'green')
                        print '[+]  {}'.format(colored(type,'blue'))
                        print ('\t _exchange: {0}\n'
                               '\t|__Preference: {1}').format(ex,pre)

                    elif type == 'SOA':
                        
                        server  = colored(str(rdata.mname).rstrip('.'),'green')
                        rname   = colored(str(rdata.rname).rstrip('.'),'green')
                        serial  = colored(rdata.serial,'green')
                        refresh = colored(rdata.refresh,'green')
                        retry   = colored(rdata.retry,'green')
                        expire  = colored(rdata.expire,'green')
                        minimum = colored(rdata.minimum,'green')

                        print '[+]  {}'.format(colored(type,'blue'))
                        print ('\t _server: {0}'
                               '\n\t|__email: {1}'
                               '\n\t|___serial: {2}'
                               '\n\t|____refresh: {3}'
                               '\n\t|_____retry: {4}'
                               '\n\t|______expire: {5}'
                               '\n\t|_______minimum ttl: {6}').format(server,rname,serial,refresh,retry,expire,minimum)
                    else:
                        print '[+]  {0} {1}'.format(colored(type,'blue'),colored(str(rdata).rstrip('.'),'green'))
            except KeyboardInterrupt:
                sys.exit(cprint('[-] Canceled by user','red'))
            except:
                pass

        ip6        = reversename.from_address(str(self.ip6))
        ip6        = str(ip6).rstrip('.')
        converter  = Convert_address(self.ip)
        converter._converting()
        (ip4_addr) = converter._return_my_addr()

        print colored('\n[*] DNS record for: {}'.format(colored(ip4_addr,'green')),'blue')

        for type in self.types:
            try:
                ans = resolver.query(ip4_addr,type)
                for rdata in ans:
                    if type == 'MX':
                        ex  = colored(str(rdata.exchange).rstrip('.'),'green')
                        pre = colored(rdata.preference,'green')
                        print '[+]  {}'.format(colored(type,'blue'))
                        print ('\t _exchange: {0}\n'
                               '\t|__Preference: {1}').format(ex,pre)

                    elif type == 'SOA':
                        
                        server  = colored(str(rdata.mname).rstrip('.'),'green')
                        rname   = colored(str(rdata.rname).rstrip('.'),'green')
                        serial  = colored(rdata.serial,'green')
                        refresh = colored(rdata.refresh,'green')
                        retry   = colored(rdata.retry,'green')
                        expire  = colored(rdata.expire,'green')
                        minimum = colored(rdata.minimum,'green')

                        print '[+]  {}'.format(colored(type,'blue'))
                        print ('\t _server: {0}'
                               '\n\t|__email: {1}'
                               '\n\t|___serial: {2}'
                               '\n\t|____refresh: {3}'
                               '\n\t|_____retry: {4}'
                               '\n\t|______expire: {5}'
                               '\n\t|_______minimum ttl: {6}').format(server,rname,serial,refresh,retry,expire,minimum)
                    else:
                        print '[+]  {0} {1}'.format(colored(type,'blue'),colored(str(rdata).rstrip('.'),'green'))
            except Exception,e:
                pass
            except KeyboardInterrupt:
                sys.exit(cprint('[-] Canceled by user','red'))

        print colored('\n[*] DNS record for: {}'.format(colored(ip6,'green')),'blue')

        for type in self.types:
            try:
                ans = resolver.query(ip6,type)
                for rdata in ans:
                    if type == 'MX':
                        ex  = colored(str(rdata.exchange).rstrip('.'),'green')
                        pre = colored(rdata.preference,'green')
                        print '[+]  {}'.format(colored(type,'blue'))
                        print ('\t _exchange: {0}\n'
                               '\t|__Preference: {1}').format(ex,pre)

                    elif type == 'SOA':
                        
                        server  = colored(str(rdata.mname).rstrip('.'),'green')
                        rname   = colored(str(rdata.rname).rstrip('.'),'green')
                        serial  = colored(rdata.serial,'green')
                        refresh = colored(rdata.refresh,'green')
                        retry   = colored(rdata.retry,'green')
                        expire  = colored(rdata.expire,'green')
                        minimum = colored(rdata.minimum,'green')

                        print '[+]  {}'.format(colored(type,'blue'))
                        print ('\t _server: {0}'
                               '\n\t|__email: {1}'
                               '\n\t|___serial: {2}'
                               '\n\t|____refresh: {3}'
                               '\n\t|_____retry: {4}'
                               '\n\t|______expire: {5}'
                               '\n\t|_______minimum ttl: {6}').format(server,rname,serial,refresh,retry,expire,minimum)
                    else:
                        print '[+]  {0} {1}'.format(colored(type,'blue'),colored(str(rdata).rstrip('.'),'green'))
            except Exception:
                pass
            except KeyboardInterrupt:
                sys.exit(cprint('[-] Canceled by user','red'))

    def zonetransfer(self):
        datas=[]
        try:
            ans=resolver.query(self.d,'NS')
        except:
            sys.exit(cprint('Zone transfer not found','red'))

        for data in ans:
            data=str(data).rstrip('.')
            datas.append(data)

        for d in datas:
            try:
                myzone = zone.from_xfr(query.xfr(d,self.d))
                if myzone:
                    for name,node in zone.nodes.items():
                        dataset=node.rdatasets
                        for record in dataset:
                            name = str(name)
                            if name != '@' and name != '*':
                                print colored(name,'blue')+colored('.','blue')+colored(self.d,'blue')
                            else:
                                pass
                else:
                    pass
            except Exception,e:
                if 'No answer or RRset not for qname' in e:
                    print colored('[-] No anwser for zone transfer','red')
                else:
                    print colored('[-] Zone transfer not found','red')
            except KeyboardInterrupt:
                sys.exit(cprint('[-] Canceled by user','red'))

