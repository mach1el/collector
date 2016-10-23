import re
import sys
import string
import requests
from termcolor import cprint,colored
from ResultParser.Counter import Counter
from ResultParser.ResultParser import Parser
from ResultParser.SkipValue import SkipValue


class search_gplus:
	def __init__(self,domain,uagent):
		self.domain    = domain
		self.uagent    = uagent
		self.re 	   = ''
		self.totre     = ''
		self.server    = 'www.google.com'
		self.start     = 0
		self.counter   = Counter()
		self.skip_user = SkipValue()
		self.users 	   = []

	def do_search(self):
		try:
			my_url = "https://" + self.server + "/search?num=100&start=" + str(self.start) + "&hl=en&meta=&q=site%3Aplus.google.com%20intext%3A%22Works%20at%22%20" + self.domain + "%20-inurl%3Aphotos%20-inurl%3Aabout%20-inurl%3Aposts%20-inurl%3Aplusones"
			try:
				headers = {'User-Agent' : self.uagent}
				r = requests.get(my_url,headers=headers)
			except Exception,e:
				raise Exception(e)
			self.re     = r.content
			self.totre += self.re

			parser      = Parser(self.totre,self.domain,self.counter)
			self.users += parser._Parser__Gplus_parser()

		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))

	def process(self):
		while self.start < 600:
			print '[*]\tSearching start with %d results' % self.start
			self.do_search()
			self.start += 100

		for user in self.users:
			self.skip_user._skip(user)
		users = self.skip_user._return_list()

		for user in users:
			print '[+] {}'.format(colored(user,'green'))