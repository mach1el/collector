#! -*- coding:utf-8 -*-

class CS:
	
	red    = '\033[91m'
	blue   = '\033[94m'
	yellow = '\033[93m'

class MethodError(object):
	def __init__(self,error=False):
		self.error = CS.red + error

	def __str__(self):
		return (CS.yellow + '[-] Your ') + self.error + (CS.yellow + ' method was not correct with other.')

class ProcessCannceled(KeyboardInterrupt):
	def __init__(self,process=False):
		self.process = CS.blue + process

	def __str__(self):
		return (CS.yellow + '[-] You have canneled your ') + self.process + (CS.yellow + ' process')