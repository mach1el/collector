#! -*- coding:utf-8 -*-

import sys
import httplib
from random import *
from termcolor import colored,cprint
sys.dont_write_bytecode=True

class UrlChecker:
	def __init__(self,url):
		self.url         	= url
		self.http_port   	= 80
		self.ssl_port    	= 443
		self.conn1          = ""
		self.conn2          = ""

	def __Check_http(self):
		try:
			self.conn1 = httplib.HTTPConnection(self.url,self.http_port)
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))
		except Exception:
			return 'Failed'
		else:
			return 'Succeed'

	def __Check_https(self):
		try:
			self.conn2 = httplib.HTTPSConnection(self.url,self.ssl_port)
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))
		except Exception:
			return 'Failed'
		else:
			return 'Succeed'