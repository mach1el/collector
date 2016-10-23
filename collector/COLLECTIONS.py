import re
import os
import sys
import time
import json
import string
import struct
import select
import httplib
import operator
import platform
from random import *
from socket import *
from threading import *
from Queue import Queue
from pprint import pprint
from datetime import datetime
from time import gmtime,strftime
from argparse import ArgumentParser,RawTextHelpFormatter

OS=platform.platform()
os_name=os.name


if os_name == 'posix':
    c = os.system('which pip')
    if c == 256:
        if 'Ubuntu' or 'Lubuntu' or 'Kubuntu' or 'Xubuntu' or 'Mint' or 'Debian' or 'Ubuntu-Mate' or 'Lxle' or 'Linux-Lite' or 'Tails' or 'Kali-Linux' or 'Peppermint' or 'Bodhi-Linux' or 'Netrunner' or 'Cub-Linux' or 'Ubuntu-Gnome' or 'Ubuntu-Studio' or 'Backbox' in OS:
            os.system('sudo apt-get install python-pip -y')
        elif 'Fedora' or 'Redhat' or 'CentOS' in OS:
            os.system('sudo yum install python-pip -y')
        elif 'Arch' or 'Manrajo' in OS:
            os.system('sudo pacman -S python-pip -y')
        else:
            print '[-] Try to download and install pip'
    else:
        pass
else:
    pass
    
try:
    import requests
    import colorama
    from bs4 import *
    from dns import resolver
    from dns import zone,query
    from dns import reversename
    from tabulate import tabulate
    from prettytable import PrettyTable
    from termcolor import colored,cprint
except:
    if os_name == 'posix':
        try:
            os.system('sudo pip install requests colorama termcolor bs4 dnspython lxml prettytable tabulate')
        except Exception,e:
            sys.exit(cprint(e,'red'))
            
    elif os_name == 'nt':
        try:
            os.system('c:\python27\scripts\pip.exe install requests colorama termcolor bs4 dnspython lxml prettytable tabulate')
        except Exception,e:
            sys.exit(cprint(e,'red'))
    else:
        sys.exit('[!] Try to download modules which was required')

try:
    import pcap
    import PyQt4
except:
    if 'Ubuntu' or 'Lubuntu' or 'Kubuntu' or 'Xubuntu' or 'Mint' or 'Debian' or 'Ubuntu-Mate' or 'Lxle' or 'Linux-Lite' or 'Tails' or 'Kali-Linux' or 'Peppermint' or 'Bodhi-Linux' or 'Netrunner' or 'Cub-Linux' or 'Ubuntu-Gnome' or 'Ubuntu-Studio' or 'Backbox' in OS:
        os.system('sudo apt-get install python-dev python-libpcap python-qt4 -y')
        sys.exit(1)
    elif 'Fedora' or 'Redhat' or 'CentOS' in OS:
        os.system('sudo yum install python-libpcap python-qt4 -y')
    elif 'Arch' or 'Manrajo' in OS:
        os.system('sudo pacman -S python-dev python-libpcap python-qt4 -y')
        sys.exit(1)
    else:
        sys.exit('[!] Try to download and install pcap module')
        sys.exit(1)

try:
    from pWhois import Pw
    from Pinger import IPPinger
    from DNSLookup import lookup_dns
    from Traceroute import Traceroute
    from EmailHunter import EmailHunter
    from SubScan import SubScan,SubWordList
    from SNSE import Tsearch,Lsearch,Gplus
    from PortScanner import xmascan,ackscan,finscan,udpscan,connscan,nullscan,stealthscan
except ImportError,e:
    raise ImportError(e)
sys.dont_write_bytecode=True
