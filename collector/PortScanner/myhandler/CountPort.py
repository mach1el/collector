import sys
sys.dont_write_bytecode=True

class CountPort:
	def __init__(self):
		self.open_port 			= 0
		self.closed_port 		= 0
		self.open_filtered_port = 0

	def StartCount(self,type):
		if type == 0:
			self.open_filtered_port+=1
		elif type == 1:
			self.closed_port+=1
		else:
			self.open_filtered_port+=1

	def Result(self):
		return (self.open_port,self.closed_port,self.open_filtered_port)