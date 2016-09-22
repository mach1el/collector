import sys
sys.dont_write_bytecode=True

class SkipValue(object):
	def __init__(self):
		self.value_to_skip = []

	def _skip(self,val):
		if val not in self.value_to_skip:
			self.value_to_skip.append(val)

	def _return_list(self):
		return self.value_to_skip