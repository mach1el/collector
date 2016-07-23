#!/usr/bin/python


version='2.0'
title = '''
       _|_|_|            _|  _|                        _|                          
     _|          _|_|    _|  _|    _|_|      _|_|_|  _|_|_|_|    _|_|    _|  _|_|  
     _|        _|    _|  _|  _|  _|_|_|_|  _|          _|      _|    _|  _|_|      
     _|        _|    _|  _|  _|  _|        _|          _|      _|    _|  _|        
      |_|_|_|    _|_|    _|  _|    _|_|_|    _|_|_|      _|_|    _|_|    _|

Author: ___T7hM1___
Github: http://github.com/t7hm1
Version:'''+version+'''
Collector python scipt which useful to collector information.It made for information gathering
'''

import re
import os;os_name=os.name
import httplib
import sys
import platform;OS=platform.platform()
import string
import time
import json
from random import *
from socket import *
from dns import resolver
from dns import reversename
from dns import zone,query
from argparse import ArgumentParser,RawTextHelpFormatter
if os_name == 'posix':
	c = os.system('which pip')
	if c == 256:
		sys.exit('[!] Try to download python pip')
	else:
		pass
else:
	pass
try:
	import requests
	import colorama
	from bs4 import *
	from termcolor import colored,cprint
	from tabulate import tabulate
except:
	if os_name == 'posix':
		if 'Ubuntu' or 'Mint' or 'Debian' or 'Kubuntu' or 'Xubuntu' or 'Lubuntu'  in OS:
			os.system('sudo pip install requests colorama termcolor tabulate bs4')
			sys.exit('[!] I have installed nessecary modules,you can run this script now')
		elif 'Fedora' or 'Redhat' or 'CentOS' in OS:
			os.system('sudo pip install requests colorama termcolor tabulate bs4')
			sys.exit('[!] I have installed nessecary modules,you can run this script now')
		elif 'Arch' or 'Manrajo' in OS:
			os.system('sudo pip install requests colorama termcolor tabulate bs4')
			sys.exit('[!] I have installed nessecary modules,you can run this script now')
		else:
			sys.exit('[!] Try to download and install all modules: requests,colorama,termcolor,tabulate')
	elif os_name == 'nt':
		os.system('c:\python27\scripts\pip.exe install requests colorama termcolor tabulate bs4')
		sys.exit('[!] I have installed nessecary modules,you can run this script now')
	else:
		sys.exit('[!] Try to download somethig which was required')

if os_name == 'nt':
	colorama.init()

def ua():
	u=[]
	u.append('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0')
	u.append('Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0')
	u.append('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0')
	u.append('Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36')
	u.append('Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36')
	u.append('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36')
	u.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27')
	return u

def check_file(f):
	try:
		file = open(f)
	except IOError,e:
		cprint('[-]'+e,'red')

def check_target(t):
	try:
		gethostbyname(t)
	except:
		sys.exit(cprint('[-] Couldn\'t resolve your target','red'))
	return True

class get_header:
	def __init__(self,d):
		self.d = d
		self.r = None
		self.request()
	def request(self):
		url = 'http://'+self.d
		self.r=requests.get(url,headers={'User-Agent':choice(ua())})
	def res(self):
		self.request()
		header = self.r.headers.items()
		code = self.r.status_code
		reason = self.r.reason
		print colored('Code: ','blue')+colored(code,'green')+'\t\t'+colored('Status: ','blue')+colored(reason,'green')
		print '-' * 40
		for x in range(len(header)):
			print ': '.join(header[x])
		print '-' * 40

class Find_twitter:
	def __init__(self,d):
		self.d = d
		self.res = ''
		self.tot_res = ''
		self.search()
	def search(self):
		url = 'https://www.google.com/search?num=100&start=0&hl=en&meta=&q=site%3Atwitter.com%20intitle%3A%22on+Twitter%22%20'+self.d
		try:
			r=requests.get(url,headers={'User-Agent':choice(ua())})
		except Exception,e:
			cprint(e,'red')
		self.res = r.content
		self.tot_res += self.res
	def clean(self):
		engine = re.compile('(@[a-zA-Z0-9._ -]*)')
		people = engine.findall(self.tot_res)
		for x in people:
			user = string.replace(x, ' | LinkedIn','')
			user = string.replace(user, ' profiles','')
			user = string.replace(user, 'LinkedIn','')
			user = string.replace(user,'"','')
			user = string.replace(user,'>','')
			if user != " ":
				cprint(user,'green')

class Search_linkedin:
	def __init__(self,d):
		self.d=d
		self.res=''
		self.tot_res=''
		self.search()
	def search(self):
		url="http://www.google.com/search?num=100&start=0&hl=en&meta=&q=site%3Alinkedin.com/in%20" + self.d
		try:
			r=requests.get(url,headers={'User-Agent':choice(ua())})
		except Exception,e:
			cprint(e,'red')
		self.res = r.content
		self.tot_res += self.res
	def clean(self):
		engine = re.compile('">[a-zA-Z0-9._ -]* \| LinkedIn')
		people = engine.findall(self.tot_res)
		for x in people:
			y = string.replace(x, ' | LinkedIn','')
			y = string.replace(y, ' profiles','')
			y = string.replace(y, 'LinkedIn','')
			y = string.replace(y, '"','')
			y = string.replace(y, '>','')
			if y != " ":
				cprint(y,'green')

class lookup_dns:
	def __init__(self,d):
		self.d=d
		self.types = [
		     "A","AAAA","AFSDB","APL","CAA","CDNSKEY","CDS","CERT",
		     "CNAME","DHCID","DLV","DNAME","DNSKEY","DS","HIP","IPSECKEY",
		     "KEY","KX","LOC","MX","NAPTR","NS","NSEC","NSEC3","NSEC3PARAM",
		     "PTR","RRSIG","RP","SIG","SOA","SRB","SSHFP","TA","TKEY","TLSA",
		     "TSIG","TXT","*","AXFR","IXFR","OPT"
		]
		self.some()
	def some(self):
		try:
			ip=gethostbyname(self.d)
		except Exception,e:
			cprint(e,'red')
		try:
			name= reversename.from_address(ip)
		except:
			name=ip
		print colored('Name:','blue'),colored(name,'green')
		print colored('IP Address:','blue'),colored(ip,'green')
	def look_up(self):
		for tp in self.types:
			try:
				ans=resolver.query(self.d,tp)
				for data in ans:
					print colored('-> Get answer from:','yellow'),colored(tp,'green')
					cprint(data,'green')
			except Exception:
				pass
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
				zonetransfer=zone.from_xfr(query.xfr(d,self.domain))
			except:
				sys.exit(cprint('Zone transfer not found','red'))
			if zonetransfer:
				for name,node in zone.nodes.items():
					dataset=node.rdatasets
					for record in dataset:
						name = str(name)
						if name != '@' and name != '*':
							print colored(name,'blue')+colored('.','blue')+colored(self.d,'blue')

class Whois:
	def __init__(self,d):
		self.d=d
		self.server='http://dazzlepod.com/ip/?ip_address='
		self.jsonf='http://dazzlepod.com/ip/'
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
	def whois(self):
		try:
			time.sleep(60)
			r=requests.get(self.server+self.d)
			rs=r.content
		except Exception,e:
			cprint(e,'red')
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))
		soup=BeautifulSoup(rs,'lxml')
		for x in soup.findAll('div',{'id':'whois-result'}):
			x=re.sub('</div>','',str(x))
			x=re.sub('<pre>','',str(x))
			x=re.sub('</pre>','',str(x))
			x=re.sub('<div id="whois-result">','',str(x))
			print x
			print '-' * 35
			print
		for x in soup.findAll('div',{'id':'scan-result'}):
			x=re.sub('</div>','',str(x))
			x=re.sub('<pre>','',str(x))
			x=re.sub('</pre>','',str(x))
			x=re.sub('<div id="scan-result">','',str(x))
			print x

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
								print colored(ipaddr,'blue').ljust(30)+colored(alias,'green')
								self.i+=1
							except:pass
					hostname = soc[0]
					for ipaddr in soc[2]:
						print colored(ipaddr,'cyan').ljust(30)+colored(hostname,'yellow')
						self.i+=1
				except:
					pass
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))
	def get_http_response(self):
		url = 'http://'+ self.host
		try:
			self.res = requests.get(url,headers={'User-Agent': choice(ua())})
		except:
			return False
	def code(self):
		return self.res.status_code
	def reason(self):
		return self.res.reason
	def headers(self):
		return self.res.headers
	def end(self):
		print '[*] Have done scan'
		print '[*] Found '+ colored(self.i,'white') + ' subdomain(s)'

class Engine:
	def __init__(self,res,d):
		self.res = res
		self.d = d
		self.host = []
	def genericClean(self):
		self.res = re.sub('<b>','',self.res)
		self.res = re.sub('</b>','',self.res)
		self.res = re.sub('<em>','',self.res)
		self.res = re.sub('</em>','',self.res)
		self.res = re.sub('<wbr>','',self.res)
		self.res = re.sub('</wbr>','',self.res)
		self.res = re.sub('<strong>','',self.res)
		self.res = re.sub('</strong>','',self.res)
		self.res = re.sub('%2f',' ',self.res)
		self.res = re.sub('%3a',' ',self.res)
		for e in ('>','<',':',';','/','\\','&','%3A','%3D','%3C'):
			self.res = string.replace(self.res,e,' ')
	def emails(self):
		self.genericClean()
		e1 = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%+-]+' + self.d,self.res)
		e2 = re.findall(r'[a-zA-Z0-9._%+-]+@'+self.d,self.res)
		e3 = re.findall(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)' + self.d,self.res)
		e = set(e1+e2+e3)
		tot = [x for x in e]
		if len(tot) == 0:
			pass
		else:
			for email in tot:
				cprint(email,'green')

class Email_searcher:
	def __init__(self,d):
		self.d = d
		self.res = ''
		self.tot_res = ''
	def google_search(self):
		url = 'http://www.google.com/search?num=100&start=0&hl=en&meta=&q=%40\"'+self.d+'\"'
		try:
			r = requests.get(url,headers={'User-Agent':choice(ua())})
		except Exception,e:
			cprint(e,'red')
		self.res = r.content
		self.tot_res+=self.res
	def bing_search(self):
		search=httplib.HTTP('www.bing.com')
		search.putrequest('GET','/search?q=%40'+self.d+'&count=50&first=0')
		search.putheader('Host','www.bing.com')
		search.putheader('Cookie','SRCHHPGUSR=ADLT=DEMOTE&NRSLT=50')
		search.putheader('Accept-Language','en-us,en')
		search.putheader('User-Agent',choice(ua()))
		search.endheaders()
		search.getreply()
		self.res = search.getfile().read()
		self.tot_res+=self.res
	def pgp_search(self):
		search=httplib.HTTP('pgp.rediris.es:11371')
		search.putrequest('GET','/pks/lookup?search='+self.d+'&op=index')
		search.putheader('Host','pgp.rediris.es')
		search.putheader('User-Agent',choice(ua()))
		search.endheaders()
		search.getreply()
		self.res = search.getfile().read()
		self.tot_res=self.res
	def exalead_search(self):
		search=httplib.HTTP('www.exalead.com')
		search.putrequest('GET','/search/web/results/?q=%40'+self.d+'&elements_per_page=50&star_index=0')
		search.putheader('Host','www.exalead.com')
		search.putheader('Referer','http://www.exalead.com/search/web/result/?q=40'+self.d)
		search.putheader('User-Agent',choice(ua()))
		search.endheaders()
		search.getreply()
		self.res = search.getfile().read()
		self.tot_res+=self.res
	def clean(self):
		self.google_search()
		worker1 = Engine(self.tot_res,self.d)
		worker1.emails()
		self.bing_search()
		worker2 = Engine(self.tot_res,self.d)
		worker2.emails()
		self.pgp_search()
		worker3 = Engine(self.tot_res,self.d)
		worker3.emails()
		self.exalead_search()
		worker4 = Engine(self.tot_res,self.d)
		worker4.emails()

class Resolver:
	def __init__(self,d):
		self.d=d
		self.ips=[]
		self.skip = []
		self.tot_ips = None
		self.server='http://iplist.net/'
	def get_ip(self):
		return gethostbyname(self.d)
	def first(self):
		self.skip.append(self.get_ip())
		try:
			r=requests.get(self.server+self.get_ip())
			rs=r.content
		except Exception,e:
			cprint(e,'red')
		soup=BeautifulSoup(rs,'lxml')
		for x in soup.findAll('a'):
			self.ips.append(x.get('href'))
		urls=re.findall('<h2>(.*?)</h2>',str(soup))
		for url in urls:
			try:
				ip=gethostbyname(url)
				print colored(ip,'blue').ljust(30)+colored(url,'green')
			except Exception:
				pass
		self.second()
	def second(self):
		i=self.skip[0]
		i=i[0:3]
		ips=[]
		for x in self.ips:
			if x.startswith('/'+i):
				if '/' in x:
					c=x.replace('/','')
					if c not in self.skip:
						ips.append(c)
					else:
						pass
		self.ips=[]
		for x in ips:
			self.skip.append(x)
			try:
				r=requests.get(self.server+x)
				rs=r.content
				soup=BeautifulSoup(rs,'lxml')
				for x in soup.findAll('a'):
					self.ips.append(x.get('href'))
				urls=re.findall('<h2>(.*?)</h2>',str(soup))
				for url in urls:
					try:
						ip=gethostbyname(url)
						print colored(ip,'blue').ljust(30)+colored(url,'green')
					except Exception:
						pass
			except Exception,e:
				cprint(e,'red')
		self.third()
	def third(self):
		i=self.skip[0]
		i=i[0:3]
		ips=[]
		for x in self.ips:
			if x.startswith('/'+i):
				if '/' in x:
					c=x.replace('/','')
					if c not in self.skip:
						ips.append(c)
					else:
						pass
		self.ips=[]
		for x in ips:
			self.skip.append(x)
			try:
				r=requests.get(self.server+x)
				rs=r.content
				soup=BeautifulSoup(rs,'lxml')
				for x in soup.findAll('a'):
					self.ips.append(x.get('href'))
				urls=re.findall('<h2>(.*?)</h2>',str(soup))
				for url in urls:
					try:
						ip=gethostbyname(url)
						print colored(ip,'blue').ljust(30)+colored(url,'green')
					except Exception:
						pass
			except Exception,e:
				cprint(e,'red')
		self.four()
	def four(self):
		i=self.skip[0]
		i=i[0:3]
		ips=[]
		for x in self.ips:
			if x.startswith('/'+i):
				if '/' in x:
					c=x.replace('/','')
					if c not in self.skip:
						ips.append(c)
					else:
						pass
		self.ips=[]
		for x in ips:
			self.skip.append(x)
			try:
				r=requests.get(self.server+x)
				rs=r.content
				soup=BeautifulSoup(rs,'lxml')
				for x in soup.findAll('a'):
					self.ips.append(x.get('href'))
				urls=re.findall('<h2>(.*?)</h2>',str(soup))
				for url in urls:
					try:
						ip=gethostbyname(url)
						print colored(ip,'blue').ljust(30)+colored(url,'green')
					except Exception:
						pass
			except Exception,e:
				cprint(e,'red')
		self.five()
	def five(self):
		i=self.skip[0]
		i=i[0:3]
		ips=[]
		for x in self.ips:
			if x.startswith('/'+i):
				if '/' in x:
					c=x.replace('/','')
					if c not in self.skip:
						ips.append(c)
					else:
						pass
		self.ips=[]
		for x in ips:
			self.skip.append(x)
			try:
				r=requests.get(self.server+x)
				rs=r.content
				soup=BeautifulSoup(rs,'lxml')
				for x in soup.findAll('a'):
					self.ips.append(x.get('href'))
				urls=re.findall('<h2>(.*?)</h2>',str(soup))
				for url in urls:
					try:
						ip=gethostbyname(url)
						print colored(ip,'blue').ljust(30)+colored(url,'green')
					except Exception:
						pass
			except Exception,e:
				cprint(e,'red')
		self.six()
	def six(self):
		i=self.skip[0]
		i=i[0:3]
		ips=[]
		for x in self.ips:
			if x.startswith('/'+i):
				if '/' in x:
					c=x.replace('/','')
					if c not in self.skip:
						ips.append(c)
					else:
						pass
		self.ips=[]
		for x in ips:
			self.skip.append(x)
			try:
				r=requests.get(self.server+x)
				rs=r.content
				soup=BeautifulSoup(rs,'lxml')
				for x in soup.findAll('a'):
					self.ips.append(x.get('href'))
				urls=re.findall('<h2>(.*?)</h2>',str(soup))
				for url in urls:
					try:
						ip=gethostbyname(url)
						print colored(ip,'blue').ljust(30)+colored(url,'green')
					except Exception:
						pass
			except Exception,e:
				cprint(e,'red')
		self.seven()
	def seven(self):
		i=self.skip[0]
		i=i[0:3]
		ips=[]
		for x in self.ips:
			if x.startswith('/'+i):
				if '/' in x:
					c=x.replace('/','')
					if c not in self.skip:
						ips.append(c)
					else:
						pass
		self.ips=[]
		for x in ips:
			self.skip.append(x)
			try:
				r=requests.get(self.server+x)
				rs=r.content
				soup=BeautifulSoup(rs,'lxml')
				for x in soup.findAll('a'):
					self.ips.append(x.get('href'))
				urls=re.findall('<h2>(.*?)</h2>',str(soup))
				for url in urls:
					try:
						ip=gethostbyname(url)
						print colored(ip,'blue').ljust(30)+colored(url,'green')
					except Exception:
						pass
			except Exception,e:
				cprint(e,'red')
		self.eight()
	def eight(self):
		i=self.skip[0]
		i=i[0:3]
		ips=[]
		for x in self.ips:
			if x.startswith('/'+i):
				if '/' in x:
					c=x.replace('/','')
					if c not in self.skip:
						ips.append(c)
					else:
						pass
		self.ips=[]
		for x in ips:
			self.skip.append(x)
			try:
				r=requests.get(self.server+x)
				rs=r.content
				soup=BeautifulSoup(rs,'lxml')
				for x in soup.findAll('a'):
					self.ips.append(x.get('href'))
				urls=re.findall('<h2>(.*?)</h2>',str(soup))
				for url in urls:
					try:
						ip=gethostbyname(url)
						print colored(ip,'blue').ljust(30)+colored(url,'green')
					except Exception:
						pass
			except Exception,e:
				cprint(e,'red')
		self.night()
	def night(self):
		i=self.skip[0]
		i=i[0:3]
		ips=[]
		for x in self.ips:
			if x.startswith('/'+i):
				if '/' in x:
					c=x.replace('/','')
					if c not in self.skip:
						ips.append(c)
					else:
						pass
		self.ips=[]
		for x in ips:
			self.skip.append(x)
			try:
				r=requests.get(self.server+x)
				rs=r.content
				soup=BeautifulSoup(rs,'lxml')
				for x in soup.findAll('a'):
					self.ips.append(x.get('href'))
				urls=re.findall('<h2>(.*?)</h2>',str(soup))
				for url in urls:
					try:
						ip=gethostbyname(url)
						print colored(ip,'blue').ljust(30)+colored(url,'green')
					except Exception:
						pass
			except Exception,e:
				cprint(e,'red')
		self.ten()
	def ten(self):
		i=self.skip[0]
		i=i[0:3]
		ips=[]
		for x in self.ips:
			if x.startswith('/'+i):
				if '/' in x:
					c=x.replace('/','')
					if c not in self.skip:
						ips.append(c)
		for x in ips:
			try:
				r=requests.get(self.server+x)
				rs=r.content
				soup=BeautifulSoup(rs,'lxml')
				urls=re.findall('<h2>(.*?)</h2>',str(soup))
				for url in urls:
					try:
						ip=gethostbyname(url)
						print colored(ip,'blue').ljust(30)+colored(url,'green')
					except Exception:
						pass
			except Exception,e:
				cprint(e,'red')

def print_result(args):
	print title
	global Runner
	fnv = ['Field','Value']
	host = args.d
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
	print tabulate(header.items(),fnv,tablefmt='orgtbl')
	print
	cprint ('Get subdomain of target','yellow')
	print 
	print 'IP Address'.ljust(22)+'Domain Name'
	print '-----------'.ljust(22)+'------------'
	Runner.scan_sub()
	Runner.end()

def main():
	parser = ArgumentParser(
		usage='./%(prog)s -d [domain] [OPTIONS]',
		version=version,
		formatter_class=RawTextHelpFormatter,
		prog='collector',
		description=title,
		epilog = '''\
Example:
     ./%(prog)s -d example.com --getheader
     ./%(prog)s -d google.com --subscan -f /path/to/wordlist
     ./%(prog)s -d apple.com --gemail --linkedin
''')
	options = parser.add_argument_group('options','')
	options.add_argument('-d',metavar='<domain>',help='Specify target domain,it look like google.com',default=False)
	options.add_argument('-f',metavar='<file>',help='Optional to choose default wordlist or custom wordlist',default='wordlist.txt')
	options.add_argument('--subscan',action='store_true',help='Enable subdomain scan')
	options.add_argument('--resolver',action='store_true',help='Resolve host name')
	options.add_argument('--lookup',action='store_true',help='Lookup Domain')
	options.add_argument('--whois',action='store_true',help='Whois your target')
	options.add_argument('--gemail',action='store_true',help='Enable emails searcher')
	options.add_argument('--gtwitter',action='store_true',help='Enable twitter searcher')
	options.add_argument('--linkedin',action='store_true',help='Enable search people in linkedin')
	options.add_argument('--getheader',action='store_true',help='Get a few information with headers')
	args = parser.parse_args()
	if args.d == False:
		parser.print_help()
		sys.exit()
	if args.d:
		t = args.d
		check_target(t)
	print title
	if args.getheader:
		cprint('[+] Get headers','yellow')
		cprint('===============\n','yellow')
		worker = get_header(args.d)
		worker.res()
	if args.lookup:
		worker = lookup_dns(args.d)
		cprint('[+] Lookup Domain','yellow')
		cprint('=================','yellow')
		worker.look_up()
		worker.zonetransfer()
	if args.whois:
		cprint('[+] Whois your target !','yellow')
		cprint('=======================','yellow')
		worker = Whois(args.d)
		worker.whois()
	if args.resolver:
		try:
			worker=Resolver(args.d)
			cprint('[+] Resolve hostname','yellow')
			cprint('====================','yellow')
			print
			print colored('IP','blue').ljust(30)+colored('Host Name','blue')
			print colored('------------','yellow').ljust(30)+colored('------------','yellow')
			worker.first()
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))
	if args.gemail:
		try:
			worker=Email_searcher(args.d)
			cprint('[+] Seaching Email(s)...','yellow')
			cprint('========================\n','yellow')
			worker.clean()
			print
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))
	if args.gtwitter:
		worker = Find_twitter(args.d)
		cprint('[+] Find twitter user(s)','yellow')
		cprint('========================','yellow')
		worker.clean()
	if args.linkedin:
		print
		worker=Search_linkedin(args.d)
		cprint('[+] Find people Linkedin','yellow')
		cprint('========================','yellow')
		worker.clean()
	if args.subscan:
		print_result(args)
	if not (args.subscan) and not (args.getheader) and not (args.gemail) and not (args.gtwitter) and not (args.linkedin) and not (args.resolver) and not (args.lookup) and not (args.whois):
		parser.print_help()
		sys.exit(cprint('[-] You must choose some option(s)','red'))

if __name__ == '__main__':
	main()
