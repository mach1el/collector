import sys
sys.dont_write_bytecode=True


class SkipPort(object):
	def __init__(self):
		self.skipports=[]

	def _skip(self,port):
		if port not in self.skipports:
			self.skipports.append(port)
			return port
		elif port in self.skipports:
			return