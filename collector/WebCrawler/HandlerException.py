#! -*- coding:utf-8 -*-

class CS:
    RED    = '\033[91m'
    OKBLUE = '\033[94m'
    YELLOW = '\033[93m'

class RequestError(object):
	def __init__(self,url=None):
		self.url = url

	def __str__(self):
		return (CS.RED + 'Can\'t request your url: ') + (CS.YELLOW + self.url)