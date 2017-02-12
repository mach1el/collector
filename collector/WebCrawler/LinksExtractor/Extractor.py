#! -*- coding:utf-8 -*-

import re
import sys
import requests
from bs4 import BeautifulSoup
from termcolor import cprint,colored
sys.dont_write_bytecode=True

class Extraction(object):
	def __init__(self,url=None):
		super(Extraction,self).__init__()
		self.url 	 		= url
		self.links 			= []
		self.url_regex 		= re.compile('^(http|https|ftp)://')
		self.content 		= self._send_request()

	def _send_request(self,url=None):
		if url == None:
			url = self.url
		else:
			url = url
		try:
			rq = requests.get('https://'+url)
		except Exception:
			rq = requests.get('http://'+url)
		except:
			sys.exit(cprint('[-] Couldn\'t send request','red'))

		return rq.content

	def _find_links(self):
		soup = BeautifulSoup(self.content,'html.parser')

		for text in soup.find_all('a',attrs={'href':re.compile('^/')}):
			try:
				link = self.url+text['href']
				self.links.append(link)
			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user','red'))

		for link in soup.find_all('a',attrs={'href':self.url_regex}):
			try:
				self.links.append(link['href'])
			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user','red'))

		return self.links