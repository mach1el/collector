# -*- coding:utf-8 -*-
import sys
import time
sys.dont_write_bytecode=True


class ProcessBar(object):
	def __init__(self,
		        total=100,
		        prefix='Process',
		        stuffix='Completed',
		        decimals=1,
		        barLength=30):
	    self.total	    = total
	    self.prefix     = prefix
	    self.stuffix    = stuffix
	    self.decimals   = decimals
	    self.barLength  = barLength
	    self.num 		= 0

	def StartPrint(self):
		self.num+=1
		try:
			formatStr       = "{0:." + str(self.decimals) + "f}"
			percents        = formatStr.format(100 * (self.num / float(self.total)))
			filledLength    = int(round(self.barLength * (self.num) / float(self.total)))
			bar             = '█' * filledLength + '-' * (self.barLength - filledLength)
			sys.stdout.write('\r%s |%s| %s%s %s' % (self.prefix, bar, percents, '%', self.stuffix)),
			if self.num == self.total:
				sys.stdout.write('\n')
			sys.stdout.flush()
		except Exception,e:
			print e
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))
		finally:
			pass
