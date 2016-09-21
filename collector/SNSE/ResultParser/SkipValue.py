import sys
sys.dont_write_bytecode=True

class SkipValue(object):
	def __init__(self):
		self.value_to_skip = []

	def __skip(self,val):
		for x in val:
			if x not in self.value_to_skip:
				self.value_to_skip.append(val)
		return self.value_to_skip