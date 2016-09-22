import re
import sys
import string
import requests
from termcolor import colored,cprint
from ResultParser.Counter import Counter
from ResultParser.ResultParser import Parser
from ResultParser.SkipValue import SkipValue

class search_linkedin:
	def __init__(self,domain,uagent):
		self.domain     = domain
		self.uagent     = uagent
		self.server     = 'www.google.com'
		self.start      = 0
		self.result     = ''
		self.totre      = ''
		self.counter    = Counter()
		self.skip_user = SkipValue()
		self.users 	    = []

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

			parser      = Parser(self.totre,self.domain,self.counter)
			self.users += parser._Parser__Linkedin_parser()

		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))

	def process(self):
		while self.start < 600:
			try:
				print '[*]\tSearching start with %d results' % self.start
				self.do_search()
				self.start+=100
			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user','red'))

		for user in self.users:
			self.skip_user._skip(user)
		users = self.skip_user._return_list()
		for user in users:
			print '[+] {}'.format(colored(user,'green'))