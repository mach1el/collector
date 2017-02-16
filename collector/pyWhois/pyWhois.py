# -*- coding:utf-8 -*-
import re
import sys
import json
import requests
from socket import *
from tabulate import tabulate
from termcolor import colored,cprint
from SubDomainHandler import DomainHandler
from RandomServer import Random_Whois_Server
sys.dont_write_bytecode=True


class Pw:
    random_server  = Random_Whois_Server()

    def __init__(self,target):
        self.target               = target
        if self.target:
            my_handler            = DomainHandler(self.target)
        self.port                 = 43
        self.tries                = 0
        self.jsonf                = 'http://dazzlepod.com/ip/'
        self.network_whois_server = Pw.random_server._random()
        self.domain_whois_server  = 'whois.internic.com'
        self.whois_server_regex   = '(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.handled_domain       = my_handler._DomainHandler__check_domain()
        if self.handled_domain == None:
            pass
        else:
            self.target = self.handled_domain
        self.get_json()

    def ip(self):
        return gethostbyname(self.target)

    def get_json(self):
        try:
            r=requests.get(self.jsonf+self.ip()+'.json')
            rs=r.content
        except Exception,e:
            cprint(e,'red')
        data=json.loads(rs)
        print tabulate(data.items(),[colored('Field','blue'),colored('Value','blue')],tablefmt='fancy_grid')

    def Network_whois(self):
        domain = self.target.replace('http://','')
        domain = self.target.replace('https://','')
        domain = self.target.replace('www.','')
        ext    = domain.split('.')[-1]
        target_ip = gethostbyname(domain)

        print colored("\n==> Queried {0} with {1}",'yellow').format(colored(self.network_whois_server,'blue'),colored(target_ip,'blue'))

        try:
            
            sock=socket(AF_INET,SOCK_STREAM)
            sock.connect((self.network_whois_server,self.port))
            sock.send(target_ip+'\r\n')
        except Exception,e:
            cprint(e,'red')
        msg=''
        while len(msg) < 100000:
            d=sock.recv(4096)
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
        if '%ERROR:101: no entries found' in msg:
            print '[!] No result found, try another server.'
            self.network_whois_server = Pw.random_server._re_random()
            self.tries+=1
            if self.tries < 4:
                self.Network_whois()
            else:
                sys.exit(cprint('[-] No whois server for domain','red'))
        else:
            cprint(msg,'green')

    def Domain_whois(self):
        domain = self.target.replace('http://','')
        domain = self.target.replace('www.','')
        domain = self.target.replace('https://','')
        ext    = domain.split('.')[-1]

        print colored("\n==> Queried {0} with {1}",'yellow').format(colored(self.domain_whois_server,'blue'),colored(domain,'blue'))

        try:
            server_ip=gethostbyname(self.domain_whois_server)
            sock=socket(AF_INET,SOCK_STREAM)
            sock.connect((server_ip,self.port))
            sock.send(domain+'\r\n')
        except Exception,e:
            cprint(e,'red')
        msg=''
        while len(msg) < 100000:
            d=sock.recv(4096)
            if d=='':
                break
            msg+=d
        cprint(msg,'green')

        my_server = re.findall('whois'+self.whois_server_regex,msg)

        if my_server == []:
            error_text = colored('[-] Couldn\'t find Domain Whois Server for: %s','red') % domain
            sys.exit(error_text)

        else:
            print colored("==> Queried {0} with {1}",'yellow').format(colored(str(my_server).replace('[','').replace(']',''),'blue'),colored(domain,'blue'))

            for server in my_server:
                try:
                    server_ip   = gethostbyname(server)
                    sock        = socket(AF_INET,SOCK_STREAM)
                    sock.connect((server_ip,self.port))
                    sock.send(domain+'\r\n')
                except Exception,e:
                    sys.exit(cprint(e,'red'))

                msg=''
                while len(msg) < 100000:
                    d = sock.recv(4096)
                    if d == '':
                        break
                    msg+=d
                cprint(msg,'green')