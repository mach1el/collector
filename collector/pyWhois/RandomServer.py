# -*- coding:utf-8 -*-
import sys
from random import *
sys.dont_write_bytecode=True

class Random_Whois_Server(object):
	def __init__(self):
		super(Random_Whois_Server,self).__init__()
		self._whois_server = ['whois.iana.org',
							  'whois.arin.net',
							  'whois.ripe.net',
							  'whois.apnic.net',
		]

	def _random(self):
		x = randint(0,3)
		server = self._whois_server[x]
		return server

	def _re_random(self):
		return self._random()
