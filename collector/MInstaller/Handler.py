# -*- coding:utf-8 -*-

import os
import sys
from platform import platform
sys.dont_write_bytecode=True


class Handler:
	def __init__(self):
		self.os_type = os.name
		self.OS 	 = platform()

	def Install_Pip(self):
		if self.os_type == "posix":
			if 'ARCH' or 'MANJARO' in self.OS:
				status = os.system('which pip2')
			else:
				status = os.system('which pip')

			if status == 0:
				pass
			else:
				check_platform = os.system('which pacman')
				if check_platform == 0:
					os.system('sudo pacman -S python2-pip python-pip')
				else:
					check_platform = os.system('which apt-get')
					if check_platform == 0:
						os.system('sudo apt-get install python-pip -y')
					else:
						check_platform = os.system('which yum')
						if check_platform == 0:
							os.system('sudo yum -y install python-pip')
						else:
							sys.exit('[!] Try to install python-pip on your platform')

		else:
			pass

	def Install_modules(self):
		if self.os_type == 'posix':

			if 'MANJARO' or 'ARCH' in OS:
				os.system('sudo pip2 install requests colorama termcolor bs4 dnspython lxml prettytable tabulate')
			else:
				os.system('sudo pip install requests colorama termcolor bs4 dnspython lxml prettytable tabulate')

		elif self.os_type == 'nt':
			os.system('c:\python27\scripts\pip.exe install requests colorama termcolor bs4 dnspython lxml prettytable tabulate')
		else:
			sys.exit('[!] Try to download modules which was required')


	def Install_pcap_gtk(self):
		check_platform = os.system('which pacman')
		if check_platform == 0:
			os.system('sudo pacman -S pygtk && yaourt -S pylibpcap')
		else:
			check_platform = os.system('which apt-get')
			if check_platform == 0:
				os.system('sudo apt-get install python-gtk2-dev python-dev python-libpcap -y')
			else:
				check_platform = os.system('which yum')
				if check_platform == 0:
					os.system('sudo yum -y install pygtk2 pylibpcap')
				else:
					sys.exit('[!] Try to install required module on your system')

