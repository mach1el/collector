import sys
import json
import requests
from socket import *
from tabulate import tabulate
from termcolor import colored,cprint
sys.dont_write_bytecode=True


class Pw:
    def __init__(self,d):
        self.d                    = d
        self.jsonf                = 'http://dazzlepod.com/ip/'
        self.rdap                 = 'https://rdap.apnic.net/ip/'
        self.server_network_whois = 'whois.iana.org'
        self.server_domain_whois  = 'whois.eurodns.com'
        self.get_json()

    def ip(self):
        return gethostbyname(self.d)

    def get_json(self):
        try:
            r=requests.get(self.jsonf+self.ip()+'.json')
            rs=r.content
        except Exception,e:
            cprint(e,'red')
        data=json.loads(rs)
        print tabulate(data.items(),[colored('Field','blue'),colored('Value','blue')],tablefmt='fancy_grid')
    def Network_whois(self):
        cprint('[*] Whois powered by IANA','yellow')
        domain = self.d.replace('http://','')
        domain = self.d.replace('https://','')
        domain = self.d.replace('www.','')
        ext    = domain.split('.')[-1]
        try:
            sock=socket(AF_INET,SOCK_STREAM)
            sock.connect((self.server_network_whois,43))
            sock.send(domain+'\r\n')
        except Exception,e:
            cprint(e,'red')
        msg=''
        while len(msg) < 100000:
            d=sock.recv(100)
            if d=='':
                break
            msg+=d
        lines=msg.splitlines()
        for line in lines:
            if ':' in line:
                words=line.split(':')
                if 'whois.' in words[1] and 'Whois Server (port 43)' in words[0]:
                    whois=word.strip()
                    break;
        cprint(msg,'green')

    def Domain_whois(self):
        cprint('[*] Whois powered by whois.eurodns.com','yellow')
        domain = self.d.replace('http://','')
        domain = self.d.replace('www.','')
        domain = self.d.replace('https://','')
        ext    = domain.split('.')[-1]
        try:
            server_ip=gethostbyname(self.server_domain_whois)
            sock=socket(AF_INET,SOCK_STREAM)
            sock.connect((server_ip,43))
            sock.send(domain+'\r\n')
        except Exception,e:
            cprint(e,'red')
        msg=''
        while len(msg) < 100000:
            d=sock.recv(100)
            if d=='':
                break
            msg+=d
        cprint(msg,'green')
