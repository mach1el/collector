# -*- coding:utf-8 -*- 

class DomainHandler(object):
	def __init__(self,domain):
		super(DomainHandler,self).__init__()
		self.domain      = domain
		self.bypass_item = ['edu','com','biz','net','org','info','co','org','gov','med','av','dr','gen','name',
							'tel','web','tv','cr','ed','go','ac','fi','ca','ac','gob','int','mil','nom','ing',
							'ing','sld',''
		]

	def __check_domain(self):
		list = self.domain.split('.')
		if len(list) == 3:
			 if list[1] in self.bypass_item:
			 	self._return_domain(domain=None)
			 else:
			 	del_item = list.pop[1]
			 	domain = '.'.join(list)
			 	self._return_domain(domain=domain)
		else:
			self._return_domain(domain=None)

	def _return_domain(self,domain=None):
		if domain == None:
			return self.domain
		else:
			return