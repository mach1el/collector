#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Collector Tool v3.1.0 — HTTP fuzzing, link extraction, DNS, WHOIS, SNSE, subdomain and port scans
"""

import os
import sys
import argparse
import textwrap
from datetime import datetime
from socket import gethostbyname
from dataclasses import dataclass
from typing import Optional, Iterable, List
from utils import coloured, format_results
from WebCrawler import HttpMethodTester, LinkExtractor
from DNSLookup import DNSCollector, SUPPORTED_TYPES
from SNSE import run_all as snse_run
from SubScan import SubdomainScanner
from WHOIS import WhoisTool
from PortScanner import (
  ActiveAckScanner, ActiveTCPScanner, FinScanner,
  NullScanner, StealthScan, ActiveUdpScan, ActiveXmas
)

SCRIPT_NAME = os.path.basename(sys.argv[0])
SCRIPT_VERSION = "3.1.0"
USER_AGENTS: List[str] = [
  "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0",
]

def resolve_host(target: str) -> str:
  try:
    return gethostbyname(target)
  except OSError as exc:
    sys.exit(coloured(f"[-] Couldn't resolve {target}: {exc}", "red"))

class WebCrawlerTool:
  """HTTP method fuzzing & link extraction."""

  def __init__(
    self,
    host: str,
    timeout: int = 5,
    max_workers: int = 5,
    port: int = 80
  ):
    self.host = host.rstrip('/')
    self.base_url = f"http://{self.host}:{port}"
    self.extractor = LinkExtractor(
      base_urls=[self.base_url],
      timeout=timeout,
      max_workers=max_workers
    )

  def fuzz_methods(self, method: Optional[str] = None) -> None:
    tester = HttpMethodTester(
      base_url=self.base_url,
      timeout=self.extractor.timeout,
      max_workers=self.extractor.max_workers
    )
    if method and method.upper() != 'ALL':
      name, code, reason = tester._send(method.upper())
      results = {name: (code, reason)}
    else:
      results = tester.run_all()
    tester.report(results)

  def extract_links(self, outfile: Optional[str] = None) -> None:
    links = self.extractor.extract()
    if not links:
      print(coloured("[!] No links found", "yellow"))
      return
    if outfile:
      with open(outfile, 'w', encoding='utf-8') as fp:
        fp.write("\n".join(links))
    else:
      print(*links, sep='\n')
    print(coloured(f"[+] Found {len(links)} links", "green"))

@dataclass
class PortScannerTool:
  host: str
  port_range: str
  timeout: float
  threads: int
  quiet: bool = False

  def _header(self) -> None:
    ip = resolve_host(self.host)
    if not self.quiet:
      print(coloured(f"Starting Collector {SCRIPT_VERSION}", "cyan"),
            f"at {datetime.now():%Y-%m-%d %H:%M}")
      print(coloured("Scanning:", "blue"), coloured(f"{self.host} ({ip})", "green"))

  def ack(self):
    if os.geteuid() != 0:
      sys.exit(coloured("[-] Root required for ACK scan", "red"))
    self._header()
    scanner = ActiveAckScanner(
      target=self.host, prange=self.port_range,
      timeout=self.timeout, threads=self.threads
    )
    print(format_results(scanner.scan()))

  def tcp(self):
    self._header()
    ActiveTCPScanner(
      target=self.host, prange=self.port_range,
      timeout=self.timeout, threads=self.threads
    ).scan()

  def fin(self):
    self._header()
    print(format_results(
      FinScanner(
        targets=self.host, prange=self.port_range,
        timeout=self.timeout, threads=self.threads
      ).scan()
    ))

  def null(self):
    self._header()
    print(format_results(
      NullScanner(
        target=self.host, prange=self.port_range,
        timeout=self.timeout, threads=self.threads
      ).scan()
    ))

  def syn(self):
    self._header()
    print(format_results(
      StealthScan(
        target=self.host, prange=self.port_range,
        timeout=self.timeout, threads=self.threads
      ).scan()
    ))

  def udp(self):
    self._header()
    print(format_results(
      ActiveUdpScan(
        target=self.host, prange=self.port_range,
        timeout=self.timeout, threads=self.threads
      ).scan()
    ))

  def xmas(self):
    self._header()
    print(format_results(
      ActiveXmas(
        target=self.host, prange=self.port_range,
        timeout=self.timeout, threads=self.threads
      ).scan()
    ))

def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    prog=SCRIPT_NAME,
    formatter_class=lambda p: argparse.HelpFormatter(p, width=80),
    description=coloured(textwrap.dedent(
      f"Collector {SCRIPT_VERSION}\nScanning – Gathering – Collecting"
    ), "green")
  )
  parser.add_argument('-d', '--domain', required=True, help='Target domain')
  parser.add_argument('-t', '--threads', type=int, default=10)
  parser.add_argument('-q', '--quiet', action='store_true')
  parser.add_argument('-v', '--version', action='version', version=SCRIPT_VERSION)

  subs = parser.add_subparsers(dest='cmd', required=True)

  crawl = subs.add_parser('crawl', help='HTTP fuzz & link extraction')
  crawl.add_argument('--method', default=None)
  crawl.add_argument('--port', type=int, default=80)
  crawl.add_argument('--extract', action='store_true')
  crawl.add_argument('--outfile')

  scan = subs.add_parser('scan', help='Port scans')
  scan.add_argument('-p', '--ports', default='default')
  scan.add_argument('--timeout', type=float, default=0.5)
  scan.add_argument('-q', '--quiet', action='store_true')
  scan.add_argument('--tech', choices=[
    'tcp','syn','fin','ack','xmas','null','udp'
  ], default='tcp')

  sub = subs.add_parser('subscan', help='Subdomain scan')
  sub.add_argument('--wordlist')

  snse = subs.add_parser('snse', help='Social network search')
  snse.add_argument('-u', '--user-agent')
  snse.add_argument('-e', '--engine', choices=['google','bing'], default='google')

  dns = subs.add_parser('dns', help='DNS lookup')
  dns.add_argument('-t', '--type', action='append', choices=SUPPORTED_TYPES)
  dns.add_argument('--zone-transfer', action='store_true')

  whois = subs.add_parser('whois', help='WHOIS lookup')
  whois.add_argument('--ip', action='store_true')
  whois.add_argument('--net', action='store_true')
  whois.add_argument('--dom', action='store_true')

  return parser

def main(argv: Optional[Iterable[str]] = None) -> None:
  args = build_parser().parse_args(argv)
  domain = args.domain.rstrip('/')

  if args.cmd == 'crawl':
    wc = WebCrawlerTool(domain, port=args.port)
    if args.extract:
      wc.extract_links(args.outfile)
    else:
      wc.fuzz_methods(args.method)

  elif args.cmd == 'scan':
    ps = PortScannerTool(
      host=domain,
      port_range=args.ports,
      timeout=args.timeout,
      threads=args.threads,
      quiet=args.quiet
    )
    getattr(ps, args.tech)()

  elif args.cmd == 'subscan':
    wordlist = None
    if args.wordlist:
      with open(args.wordlist) as wf:
        wordlist = [l.strip() for l in wf if l.strip()]
    SubdomainScanner(
      host=domain,
      wordlist=wordlist,
      threads=args.threads,
      verbose=not args.quiet
    ).run()

  elif args.cmd == 'snse':
    snse_run(domain, args.user_agent)

  elif args.cmd == 'dns':
    dc = DNSCollector(domain, args.type)
    if args.zone_transfer:
      dc.zone_transfer()
    else:
      dc.lookup()

  elif args.cmd == 'whois':
    if not (args.ip or args.net or args.dom):
      args.ip = args.net = args.dom = True
    WhoisTool(domain, args.ip, args.net, args.dom).run()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print(coloured('\n[!] Interrupted by user', 'yellow'))