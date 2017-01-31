#! -*- coding:utf-8 -*-

import sys
import SubWordList
from socket import *
from threading import *
from Queue import Queue
from PrintProcess import ProcessBar
from prettytable import PrettyTable
from termcolor import colored,cprint
from PassSameHost import PassSameHost

h=Queue()
q=Queue()

sys.dont_write_bytecode=True

def start_pool(s,pool):
    try:
        with s:
            pool.scan_sub()
    except KeyboardInterrupt:
        sys.exit(cprint('[-] Canceled by user','red'))

class SDS(object):
    def __init__(self,host,lock,quite,PProcess,file,skip_host):
        super(SDS,self).__init__()
        self.host      = host
        self.lock      = lock
        self.quite     = quite
        self.PProcess  = PProcess
        self.file      = file
        self.skip_host = skip_host
        self.sub       = []
        self.c         = 0

    def scan_sub(self):
        try:
            if self.quite == True:
                self.PProcess.StartPrint()
            else:
                pass
            ipv4=gethostbyname(self.host)
            if ipv4:
                with self.lock:
                    self.c+=1
                    debug=gethostbyname_ex(self.host)
                    for alias in debug[1]:
                        try:
                            debug_ip=gethostbyname(alias)
                            if self.quite == False:
                                ip,host = self.skip_host._PassSameHost__Add_to_list(debug_ip,alias)
                                print colored(ip,'blue').ljust(30)+colored(host,'green')
                            else:
                                h.put((ip,host))


                            self.sub = host.split('.')
                            if self.sub[1] in SubWordList.mydict:
                                q.put(1)
                            else:
                                pass

                            if self.file != None:
                                self.file.write(debug_ip+'\t'+alias)
                                self.file.write('\n')
                            else:
                                pass
                        except:
                            pass
                    hostname=debug[0]
                    for ipaddr in debug[2]:
                        if self.quite == False:
                            ip,host=self.skip_host._PassSameHost__Add_to_list(debug_ip,alias)
                            print colored(ip,'cyan').ljust(30)+colored(host,'yellow')
                        else:
                            h.put((ip,host))

                        self.sub = host.split('.')
                        if self.sub[1] in SubWordList.mydict:
                            q.put(1)
                        else:
                            pass

                        if self.file != None:
                            self.file.write(debug_ip+'\t'+alias)
                            self.file.write('\n')
                        else:
                            pass
                    debug.close()
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))
        except:
            pass
        finally:
            pass


class SubScanner:
    def __init__(self,hosts,quite,wf=None):
        self.hosts     = hosts
        self.quite     = quite
        self.wf        = wf
        self.lock      = Lock()
        self.s         = Semaphore(100)
        self.mysubs    = []
        self.threads   = []
        self.count_sub = 0
        self.n         = 0
        self.__field   = ['IP Adress','Domain Name']
        self.__table   = PrettyTable(self.__field)
        self.PProcess  = ProcessBar(len(hosts))
        self.skip_host = PassSameHost()

    def _Start_scan(self):
        try:
            if self.wf == None:
                file = None
            else:
                file = open(self.wf,'wb+')

            for host in self.hosts:
                pool = SDS(host,self.lock,self.quite,self.PProcess,file,self.skip_host)
                t    = Thread(target=start_pool,args=(self.s,pool))
                self.threads.append(t)

            for thread in self.threads:
                thread.daemon=True
                thread.start()

            for thread in self.threads:
                thread.join()

            if self.quite == True:
                while 1:
                    if not h.empty():
                        sub = h.get()
                        self.mysubs.append(sub)
                    else:
                        break
                for data in self.mysubs:
                    self.__table.add_row(data)
                sys.stdout.write('\n\n')
                print self.__table
            else:
                pass

            while 1:
                if not q.empty():
                    num            = q.get()
                    self.count_sub += num
                else:
                    break

            print '[*] Finished scan !'
            print 'Found {} subdomains in dictionary'.format(colored(self.count_sub,'blue'))

        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user','red'))
