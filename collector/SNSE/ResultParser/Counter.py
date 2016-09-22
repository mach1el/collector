import sys
sys.dont_write_bytecode=True

class Counter(object):
	def __init__(self):
		self.mylist = []

	def _count_it(self,val):
		self.mylist += val

	def _return_list(self):
		return self.mylist