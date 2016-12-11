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
from MInstaller.Handler import Handler
from argparse import ArgumentParser,RawTextHelpFormatter
sys.dont_write_bytecode=True

minstaller = Handler()
minstaller.Install_Pip()
    
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
   minstaller.Install_modules()

try:
    import pcap
    import PyQt4
except:
    minstaller.Install_pcap_pyqt()
    sys.exit(0)
try:
    from pWhois import Pw
    from Pinger import IPPinger
    from HandlerException import *
    from DNSLookup import lookup_dns
    from Traceroute import Traceroute
    from EmailHunter import EmailHunter
    from SNSE import Tsearch,Lsearch,Gplus
    from SubScan import SubScan,SubWordList
    from WebCrawler.Tester.UrlChecker import UrlChecker
    from WebCrawler.Tester.MethodsTest import MethodsTester
    from PortScanner import xmascan,ackscan,finscan,udpscan,connscan,nullscan,stealthscan
except ImportError,e:
    raise ImportError(e)

