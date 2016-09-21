import re
import sys
import string
from SkipValue import SkipValue
from termcolor import colored,cprint
sys.dont_write_byte_code=True

class Parser:
	def __init__(self,result,domain):
		self.result = result
		self.domain = domain
		self.users  = []
		self.skip   = SkipValue()

	def __Twitter_parser(self):
		try:
			twitter_reg = re.compile('(@[a-zA-Z0-9._ -]*)')
			parse_it    = twitter_reg.findall(self.result)
			usersl 		= self.skip._SkipValue__skip(parse_it)

			for u in usersl:
				y = string.replace(u, ' | LinkedIn', '')
				y = string.replace(y, ' profiles ', '')
				y = string.replace(y, 'LinkedIn', '')
				y = string.replace(y, '"', '')
				y = string.replace(y, '>', '')
				if y != " ":
					self.users.append(y)
			return self.users
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))

	def __Linkedin_parser(self):
		try:
			linkedin_reg = re.compile('">[a-zA-Z0-9._ -]* \| LinkedIn')
			parse_it 	 = linkedin_reg.findall(self.result)
			usersl		 = self.skip._SkipValue__skip(parse_it)

			for u in usersl:
				y = string.replace(u, '| LinkedIn', '')
				y = string.replace(y, ' profiles ', '')
				y = string.replace(y, 'LinkedIn', '')
				y = string.replace(y, '"', '')
				y = string.replace(y, '>', '')
				if y != " ":
					self.users.append(y)
			return self.users
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user','red'))