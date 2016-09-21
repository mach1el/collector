import sys
from socket import *
from dns import zone
from dns import resolver
from dns import reversename
from termcolor import colored,cprint
sys.dont_write_bytecode=True

class lookup_dns:
    def __init__(self,d):
        self.d     = d
        self.types = [
             "A","AAAA","AFSDB","APL","CAA","CDNSKEY","CDS","CERT",
             "CNAME","DHCID","DLV","DNAME","DNSKEY","DS","HIP","IPSECKEY",
             "KEY","KX","LOC","MX","NAPTR","NS","NSEC","NSEC3","NSEC3PARAM",
             "PTR","RRSIG","RP","SIG","SOA","SRB","SSHFP","TA","TKEY","TLSA",
             "TSIG","TXT","*","AXFR","IXFR","OPT","SRV"
        ]
        self.name =''
    def resolve_PTR(self):
        try:
            addr=reversename.from_address(self.d)
            data=str(resolver.query(addr,'PTR')[0])
            return data
        except:
            pass
    def some(self):
        try:
            ip=gethostbyname(self.d)
        except Exception,e:
            cprint(e,'red')
        try:
            self.name=reversename.from_address(ip)
        except:
            self.name=ip
        print colored('Name:','blue'),colored(self.name,'green')
        print colored('IP Address:','blue'),colored(ip,'green')
    def look_up(self):
        for tp in self.types:
            try:
                ans=resolver.query(self.d,tp)
                for data in ans:
                    print colored('[+]  {0} {1}','blue').format(colored(tp,'blue'),colored(data,'green'))
            except Exception:
                pass
            except KeyboardInterrupt:
                sys.exit(cprint('[-] Canceled by user','red'))
        for tp in self.types:
            try:
                ans=resolver.query(self.name,tp)
                for data in ans:
                    print colored('[+]  {0} {1} ','blue').format(colored(tp,'blue'),colored(self.name,'red'))
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
                myzone=zone.from_xfr(query.xfr(d,self.domain))
            except:
                sys.exit(cprint('Zone transfer not found','red'))
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
