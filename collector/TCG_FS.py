# -*- coding:utf-8 -*-
import re
import os
import sys
import time
import platform
from random import *
from socket import *
from datetime import datetime
from time import gmtime,strftime
from MInstaller.Handler import Handler
from argparse import ArgumentParser,RawTextHelpFormatter

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
try:
    from Pinger import IPPinger
    from HandlerException import *
    from pyWhois.pyWhois import Pw
    from DNSLookup import lookup_dns
    from Traceroute import Traceroute
    from EmailHunter import EmailHunter
    from SNSE import Tsearch,Lsearch,Gplus
    from SubScan import SubScan,SubWordList
    from pyWhois.SubDomainHandler import DomainHandler
    from pyWhois.RandomServer import Random_Whois_Server
    from WebCrawler.Tester.MethodsTest import MethodsTester
    from WebCrawler.LinksExtractor import Extractor,LinksHandler,ExtractMultiLinks
    from PortScanner import xmascan,ackscan,finscan,udpscan,connscan,nullscan,stealthscan
except ImportError,e:
    raise ImportError(e)
sys.dont_write_bytecode=True
