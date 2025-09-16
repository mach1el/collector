# -*- coding: utf-8 -*-

import random
import socket
import sys
import requests
from tabulate import tabulate
from .domain_handler import DomainHandler

DEFAULT_PORT = 43
JSON_LOOKUP_URL = 'https://ipwhois.app/json'

class RandomWhoisServer:
  _SERVERS = [
    'whois.iana.org',
    'whois.arin.net',
    'whois.ripe.net',
    'whois.apnic.net',
    'whois.lacnic.net',
    'whois.afrinic.net',
  ]

  @classmethod
  def pick(cls) -> str:
    return random.choice(cls._SERVERS)

class WhoisTool:
  def __init__(self, target: str, do_ip: bool, do_net: bool, do_dom: bool):
    handler = DomainHandler(target)
    self.target = handler.get()
    self.do_ip = do_ip
    self.do_net = do_net
    self.do_dom = do_dom

  def _resolve(self) -> str:
    try:
      return socket.gethostbyname(self.target)
    except socket.gaierror as e:
      sys.exit(f"Error resolving {self.target}: {e}")

  def _lookup_json(self, ip: str):
    """Query ipwhois.app for JSON IP data and display as table."""
    try:
      resp = requests.get(f"{JSON_LOOKUP_URL}/{ip}", timeout=5)
      data = resp.json()
      if data.get('success') is False:
        msg = data.get('message', 'Unknown error')
        print(f"IP lookup failed: {msg}", file=sys.stderr)
        return

      data.pop('success', None)
      data.pop('message', None)
      print(tabulate(data.items(), headers=['Field', 'Value'], tablefmt='fancy_grid'))
    except Exception as e:
      print(f"JSON lookup failed: {e}", file=sys.stderr)

  def _whois_query(self, query: str, server: str) -> str:
    try:
      with socket.create_connection((server, DEFAULT_PORT), timeout=10) as sock:
        sock.sendall((query + "\r\n").encode())
        resp = []
        while True:
          chunk = sock.recv(4096)
          if not chunk:
            break
          resp.append(chunk.decode(errors='ignore'))
        return ''.join(resp)
    except Exception as e:
      return f"Error querying {server}: {e}"

  def run(self):
    ip = self._resolve()
    if self.do_ip:
      print(f"\n--- JSON IP Lookup for {ip} ---")
      self._lookup_json(ip)

    if self.do_net:
      server = RandomWhoisServer.pick()
      print(f"\n--- Network WHOIS ({server}) for IP {ip} ---")
      print(self._whois_query(ip, server))

    if self.do_dom:
      print(f"\n--- Domain WHOIS (internic) for {self.target} ---")
      base = 'whois.internic.net'
      resp = self._whois_query(self.target, base)
      print(resp)
      refs = [
        line.split(':',1)[1].strip()
        for line in resp.splitlines()
        if line.lower().startswith('whois server:')
      ]
      for ref in refs:
        print(f"\n--- Referred WHOIS ({ref}) for {self.target} ---")
        print(self._whois_query(self.target, ref))