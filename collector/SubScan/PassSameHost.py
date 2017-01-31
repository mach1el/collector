#! -*- coding:utf-8 -*-

import sys
sys.dont_write_bytecode=True

class PassSameHost(object):
	def __init__(self):
		self.iplist   = []
		self.hostlist = []
		super(PassSameHost,self).__init__()

	def __Add_to_list(self,ip=None,host=None):
		if ip not in self.iplist and host not in self.hostlist:
			self.iplist.append(ip)
			self.hostlist.append(host)
			return (ip,host)

		elif ip in self.iplist and host not in self.hostlist:
			self.hostlist.append(host)
			return (ip,host)

		else:
			pass