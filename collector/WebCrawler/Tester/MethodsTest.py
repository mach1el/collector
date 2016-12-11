#! -*- coding:utf-8 -*-

from random import *
from httplib import *
from termcolor import colored,cprint

class Check_Status(object):

	Informational = [100,101,102]
	Success       = range(200,300)
	Redirection   = range(300,400)
	ClientError   = range(400,500)
	ServerError   = range(500,600)

	def __init__(self):
		super(Check_Status,self).__init__()

	def _check(self,status):
		if status in Check_Status.Informational:
			return ('blue')
		elif status in Check_Status.Success:
			return ('green')
		elif status in Check_Status.Redirection:
			return ('yellow')
		elif status in Check_Status.ClientError:
			return ('red')
		elif status in Check_Status.ServerError:
			return ('red')

class MethodsTester:
	def __init__(self,url,port):
		self.url            = url
		self.port 			= port
		self.caches         = ['no-cache',
		                       'no-store',
		                       'max-age='+str(randint(0,10)),
		                       'max-stale='+str(randint(0,100)),
		                       'min-fresh='+str(randint(0,10)),
		                       'notransform',
		                       'only-if-cache'
		]
		self.AcceptEC       = ['*',
		                       'compress,gzip',
		                       'compress;q=0,5, gzip;q=1.0',
		                       'gzip;q=1.0, indentity; q=0.5, *;q=0'
		]
		self.User_Agent     = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
		                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
		                       'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
		                       'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
		                       'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
		                       'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)'
		]
		self.custom_header  = self.__Create_headers()
		self.Status_checker = Check_Status()

		if self.port == 80:
			try:
				self.Requester = HTTPConnection(self.url,80)
			except Exception,e:
				raise Exception(e)
		else:
			try:
				self.Requester = HTTPSConnection(self.url,443)
			except Exception,e:
				raise Exception(e)

	def __Create_headers(self):
		headers = {
		    'User-Agent' : choice(self.User_Agent),
		    'Cache-Control' : self.caches,
		    'Accept-Encoding' : self.AcceptEC,
		    'Keep-Alive' : '42',
		    'Connection' : 'keep-alive',
		    'Host' : self.url
		}
		return headers

	def GET(self):
		self.Requester.request('GET',self.url,None,self.custom_header)
		res = self.Requester.getresponse()
		if res:
			cprint('GET Method','cyan')
			if res.status:
				check = self.Status_checker._check(res.status)
				if check:
					print 'Status => {0}\tReason => {1}'.format(colored(res.status,check),colored(res.reason,check))
		data = res.read()
		print data+'\n'

	def HEAD(self):
		self.Requester.request('HEAD',self.url,None,self.custom_header)
		res = self.Requester.getresponse()
		if res:
			cprint('HEAD Method','cyan')
			if res.status:
				check = self.Status_checker._check(res.status)
				if check:
					print 'Status => {0}\tReason => {1}'.format(colored(res.status,check),colored(res.reason,check))
		data = res.read()
		print data+'\n'

	def POST(self):
		self.Requester.request('POST',self.url,None,self.custom_header)
		res = self.Requester.getresponse()
		if res:
			cprint('POST Method','cyan')
			if res.status:
				check = self.Status_checker._check(res.status)
				if check:
					print 'Status => {0}\tReason => {1}'.format(colored(res.status,check),colored(res.reason,check))
		data = res.read()
		print data+'\n'

	def PUT(self):
		self.Requester.request('PUT',self.url,None,self.custom_header)
		res = self.Requester.getresponse()
		if res:
			cprint('PUT Method','cyan')
			if res.status:
				check = self.Status_checker._check(res.status)
				if check:
					print 'Status => {0}\tReason => {1}'.format(colored(res.status,check),colored(res.reason,check))
		data = res.read()
		print data+'\n'

	def DELETE(self):
		self.Requester.request('DELETE',self.url,None,self.custom_header)
		res = self.Requester.getresponse()
		if res:
			cprint('DELETE Method','cyan')
			if res.status:
				check = self.Status_checker._check(res.status)
				if check:
					print 'Status => {0}\tReason => {1}'.format(colored(res.status,check),colored(res.reason,check))
		data = res.read()
		print data+'\n'

	def CONNECT(self):
		self.Requester.request('CONNECT',self.url,None,self.custom_header)
		res = self.Requester.getresponse()
		if res:
			cprint('CONNECT Method','cyan')
			if res.status:
				check = self.Status_checker._check(res.status)
				if check:
					print 'Status => {0}\tReason => {1}'.format(colored(res.status,check),colored(res.reason,check))
		data = res.read()
		print data+'\n'

	def OPTIONS(self):
		self.Requester.request('OPTIONS',self.url,None,self.custom_header)
		res = self.Requester.getresponse()
		if res:
			cprint('OPTIONS Method','cyan')
			if res.status:
				check = self.Status_checker._check(res.status)
				if check:
					print 'Status => {0}\tReason => {1}'.format(colored(res.status,check),colored(res.reason,check))
		data = res.read()
		print data+'\n'

	def TRACE(self):
		self.Requester.request('TRACE',self.url,None,self.custom_header)
		res = self.Requester.getresponse()
		if res:
			cprint('TRACE Method','cyan')
			if res.status:
				check = self.Status_checker._check(res.status)
				if check:
					print 'Status => {0}\tReason => {1}'.format(colored(res.status,check),colored(res.reason,check))
		data = res.read()
		print data+'\n'

