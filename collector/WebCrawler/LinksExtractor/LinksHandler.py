#! -*- coding:utf-8 -*-

import sys
from termcolor import cprint
sys.dont_write_bytecode=True

class LinksHandler(object):
	def __init__(self):
		self.listLink = []

	def _remake_link(self,links):
		for link in links:
			link = link.replace('http://','').replace('https://','').replace('www.','')
			self.listLink.append(link)

		return self.listLink

	def _pass_same_link(self,links):
		llink = []
		for link in links:
			try:
				if link not in llink:
					llink.append(link)
				else:
					pass
			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user','red'))
		return llink