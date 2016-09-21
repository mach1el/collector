import re
import sys
import string
import requests
from termcolor import colored,cprint
from ResultParser.ResultParser import Parser

class search_linkedin:
	def __init__(self,domain,uagent):
		self.domain = domain
		self.uagent = uagent
		self.server = 'www.google.com'
		self.start  = 0
		self.result = ''
		self.totre  = ''

	def do_search(self):
		try:
			my_url = 'https://' + self.server + '/search?num=100&start=' + str(self.start) + '&hl=en&meta=&q=site%3Alinkedin.com/in%20' + self.domain
			headers = {'User-Agent':self.uagent}
			try:
				r = requests.get(my_url,headers=headers)
			except Exception,e:
				raise Exception(e)
				self.result = r.content
				self.totre += self.result

			parser = Parser(self.totre,self.domain)
			users   = parser._Parser__Linkedin_parser()
			for user in users:
				print '[+] {}'.format(colored(user,'blue'))
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))

	def process(self):
		while self.start < 500:
			try:
				self.do_search()
				self.start+=100
				print '[*]\t\tSearching start with %d results' % self.start
				if self.start > 500:
					break
			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user','red'))