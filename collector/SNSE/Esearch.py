import re
import sys
import httplib
import string
import requests
from termcolor import cprint,colored
from ResultParser.Counter import Counter
from ResultParser.ResultParser import Parser
from ResultParser.SkipValue import SkipValue

class search_email:
    def __init__(self,domain,uagent):
        self.domain     = domain
        self.uagent     = uagent
        self.res        = ''
        self.tot_res    = ''
        self.start      = 0
        self.skip_value = SkipValue()
        self.counter    = Counter()
        self.userl      = []

    def google_search(self):
        try:
            url = 'http://www.google.com/search?num=100&start=' + str(self.start) + '+&hl=en&meta=&q=%40\"'+ self.domain +'\"'
            try:
                r = requests.get(url,headers={'User-Agent':self.uagent})
            except Exception:
                pass
            self.res = r.content
            self.tot_res+=self.res

            parser = Parser(self.tot_res,self.domain,self.counter)
            parser._Parser__Email_parser()

        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))

    def bing_search(self):
        try:
            search=httplib.HTTP('www.bing.com')
            search.putrequest('GET','/search?q=%40' + self.domain +'&count=50&first=' + str(self.start))
            search.putheader('Host','www.bing.com')
            search.putheader('Cookie','SRCHHPGUSR=ADLT=DEMOTE&NRSLT=50')
            search.putheader('Accept-Language','en-us,en')
            search.putheader('User-Agent',self.uagent)
            search.endheaders()
            search.getreply()
            self.res = search.getfile().read()
            self.tot_res+=self.res

            parser = Parser(self.tot_res,self.domain,self.counter)
            parser._Parser__Email_parser()

        except Exception:
            pass
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))

    def pgp_search(self):
        try:
            search=httplib.HTTP('pgp.rediris.es:11371')
            search.putrequest('GET','/pks/lookup?search='+self.domain +'&op=index')
            search.putheader('Host','pgp.rediris.es')
            search.putheader('User-Agent',self.uagent)
            search.endheaders()
            search.getreply()
            self.res = search.getfile().read()
            self.tot_res=self.res

            parser = Parser(self.tot_res,self.domain,self.counter)
            parser._Parser__Email_parser()

        except Exception:
            pass
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))

    def exalead_search(self):
        try:
            search=httplib.HTTP('www.exalead.com')
            search.putrequest('GET','/search/web/results/?q=%40'+ self.domain +'&elements_per_page=50&star_index='+str(self.start))
            search.putheader('Host','www.exalead.com')
            search.putheader('Referer','http://www.exalead.com/search/web/result/?q=40'+self.domain)
            search.putheader('User-Agent',self.uagent)
            search.endheaders()
            search.getreply()
            self.res = search.getfile().read()
            self.tot_res+=self.res

            parser = Parser(self.tot_res,self.domain,self.counter)
            parser._Parser__Email_parser()

        except Exception:
            pass
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))

    def process(self):
        try:
            while self.start < 600:
                print '[*]\tSearching start with %d results' % self.start
                self.google_search();
                self.bing_search();
                self.pgp_search();
                self.exalead_search();
                self.start += 100

            users =(self.counter._return_list())
            for user in users:
                self.skip_value._skip(user)
                self.userl = self.skip_value._return_list()

            self.print_result()
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))

    def print_result(self):
        try:
            for user in self.userl:
                print '[+] {}'.format(colored(user,'green'))
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))