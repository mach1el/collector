#!/usr/bin/python

import os
os_name = os.name
from socket import *
try:
	from termcolor import colored,cprint
	from tabulate import tabulate
except:
	if os_name == 'posix':
		os.system('sudo pip install termcolor')
		os.system('sudo pip install tabulate')
		print '[!] Installed termcolor and tabulate you can run this script'
	elif os_name != 'posix':
		print '[-] Download termcolor,tabulate and install'
	else:
		print '[-] You must install pip'
import httplib
import random
import sys
from argparse import ArgumentParser,RawTextHelpFormatter

def check_file(f):
	try:
		file = open(f)
	except IOError,e:
		cprint('[-]'+e,'red')


class SDC:
	def __init__(self,host,dct):
		self.host = host
		self.dct = dct
		self.subdomains = []
		self.res = None
		self.name = ''
		self.i = 0
		self.get_http_response()
	def get_ip(self):
		try:
			ip = gethostbyname(self.host)
			self.name = ip
		except:
			cprint('[-] Can\'t resolver host:Unknow host','red')
		return ip
	def get_domain_name(self):
		try:
			name = gethostbyaddr(self.name)
			return name[0]
		except:
			pass
	def scan_sub(self):
		file = open(self.dct).readlines()
		setdefaulttimeout(3)
		try:
			for words in file:
				word = words.strip('\t').strip('\n')
				domain = word+'.'+self.host
				try:
					dw = gethostbyname(domain)
					if dw:
						soc=gethostbyname_ex(domain)
						for alias in soc[1]:
							try:
								ipaddr = gethostbyname(alias)
								self.subdomains.append([colored(alias,'cyan'),colored(ipaddr,'red')])
								self.i+=1
							except:pass
					hostname = soc[0]
					for ipaddr in soc[2]:
						self.subdomains.append([hostname,ipaddr])
						self.i+=1
				except:pass
		except KeyboardInterrupt:
			exit(0)
		return self.subdomains
	def get_http_response(self):
		try:
			cnn = httplib.HTTPConnection(self.host)
			cnn.request('HEAD','/index.html')
			self.res = cnn.getresponse()
		except:
			return False
	def code(self):
		return self.res.status
	def reason(self):
		return self.res.reason
	def headers(self):
		return self.res.getheaders()
	def end(self):
		print '[*] Have done scan'
		print '[*] Found '+ colored(self.i,'white') + ' subdomain(s)'


def print_result(args):
	global Runner
	fnv = ['Field','Value']
	host = args.domain
	dct = args.file
	Runner = SDC(host,dct)
	ipaddress = Runner.get_ip();dmn = Runner.get_domain_name()
	code = Runner.code();status = Runner.reason();header = Runner.headers()
	cprint('Get target infomation','blue')
	print
	print 'IP Address'.ljust(18)+'Domain Name'
	print '----------'.ljust(18)+'-----------'
	print str(ipaddress).ljust(18)+str(dmn)
	print
	print 'Code'.ljust(18)+'Status'
	print '----------'.ljust(18)+'-----------'
	print str(code).ljust(18)+status
	print
	cprint('Get a few infomation of target\n','green')
	print tabulate(header,fnv,tablefmt='orgtbl')
	print
	cprint ('Get subdomain of target','yellow')
	print 
	print_subdomain()

def print_subdomain():
	subdomains = Runner.scan_sub()
	table = ['Domain Name','Ip Address']
	print tabulate(subdomains,table,tablefmt='fancy_grid')
	Runner.end()

def main():
	__script=colored(sys.argv[0],'blue')
	__version='2.0'
	__title='''
     ___      _    ___                 _        ___                            
    / __|_  _| |__|   \ ___ _ __  __ _(_)_ _   / __| __ __ _ _ _  _ _  ___ _ _ 
    \__ \ || | '_ \ |) / _ \ '  \/ _` | | ' \  \__ \/ _/ _` | ' \| ' \/ -_) '_|
    |___/\_,_|_.__/___/\___/_|_|_\__,_|_|_||_| |___/\__\__,_|_||_|_||_\___|_|

                                  ___T7hM1___
    Github: http://github.com/t7hm1/subscan
    Version: ''' + __version + '''
''' 
	parser = ArgumentParser(
		version=__version,
		formatter_class=RawTextHelpFormatter,
		prog='subscan',
		description=__title,
		epilog = '''\
Example:
Scan with default wordlist ''' +\
    __script + ''' google.com 
Scan with custom wordlist ''' +\
    __script + ''' nsa.gov -f /path/to/file
''')
	parser.add_argument('domain',help='Specify target domain,it look like google.com',default=False)
	parser.add_argument('-f','--file',help='Optional to choose default wordlist or custom wordlist',default='wordlist.txt')
	args = parser.parse_args()
	print_result(args)

if __name__ == '__main__':
	main()
