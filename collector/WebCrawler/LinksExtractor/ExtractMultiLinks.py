#! -*- coding:utf-8 -*-

import sys
import time
from Queue import *
from threading import *
from Extractor import Extraction
from LinksHandler import LinksHandler

sys.dont_write_bytecode=True

q=Queue()

class ExtractMultiLinks(Thread):
	def __init__(self,link):
		super(ExtractMultiLinks,self).__init__()
		self.link = link
		self.ext  = Extraction(self.link)

	def run(self):
		links   = self.ext._find_links()
		q.put(links)

class Proc:
	def __init__(self,links):
		self.links     = links
		self.listLink  = []
		self.lHandler  = LinksHandler()

	def GiveLinks(self):
		for link in self.links:
			myProc 		  = ExtractMultiLinks(link)
			myProc.daemon = True
			myProc.start()
			time.sleep(.1)

		for x in xrange(len(self.links)):
			myProc.join()

		while 1:
			if not q.empty():
				links = q.get()
				if links != None:
					self.listLink+=links
				else:
					pass
			else:
				break

		nlinks = self.lHandler._remake_link(self.listLink)
		return nlinks
