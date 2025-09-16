# -*- coding: utf-8 -*-
"""
Optimized TCP connect scanner: returns results dict for external formatting.
"""
import sys
import time
import socket
from threading import Semaphore, Thread
from queue import Queue

# Default well-known ports (1-1023)
DEFAULT_PORT_RANGE = range(1, 1024)

# Thread-safe queue for discovered ports
_open_ports = Queue()


def parse_port_range(prange):
  """Parse comma-separated ports/ranges or use DEFAULT if empty or 'default'."""
  if not prange or prange.lower() in ('default', 'well-known'):
    return DEFAULT_PORT_RANGE
  ports = []
  for part in prange.split(','):
    part = part.strip()
    if '-' in part:
      start, end = part.split('-', 1)
      try:
        start, end = int(start), int(end)
      except ValueError:
        raise ValueError('Port range must be integers')
      if start > end:
        start, end = end, start
      ports.extend(range(start, end + 1))
    else:
      try:
        ports.append(int(part))
      except ValueError:
        raise ValueError('Port must be an integer or range')
  return sorted(set(ports))

class TCPScanner(object):
  """Per-port TCP connect scan worker."""
  def __init__(self, target_ip, port, timeout):
    self.target_ip = target_ip
    self.port = port
    self.timeout = timeout

  def run(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(self.timeout)
    try:
      res = sock.connect_ex((self.target_ip, self.port))
      if res == 0:
        _open_ports.put(self.port)
    except Exception:
      pass
    finally:
      sock.close()

class ActiveTCPScanner(object):
  """Manage and dispatch TCP connect scans, returning results dict."""
  def __init__(self, target, prange='', timeout=1.0, threads=100):
    try:
      self.target_ip = socket.gethostbyname(target)
    except socket.gaierror:
      sys.exit('Invalid host: {}'.format(target))
    self.ports = parse_port_range(prange)
    self.timeout = float(timeout)
    self.semaphore = Semaphore(threads)

  def scan(self):
    """Perform scan and return {ip: [(port, status), ...]}"""
    start = time.time()
    threads = []

    for port in self.ports:
      worker = TCPScanner(self.target_ip, port, self.timeout)
      t = Thread(target=self._scan_port, args=(worker,))
      t.daemon = True
      threads.append(t)
      t.start()

    for t in threads:
      t.join()

    # Collect results
    results = {self.target_ip: []}
    while not _open_ports.empty():
      port = _open_ports.get()
      try:
        service = socket.getservbyport(port)
      except:
        service = ''
      results[self.target_ip].append((port, 'open', service))

    elapsed = time.time() - start
    # Optionally log or return timing
    results['_elapsed'] = elapsed
    return results

  def _scan_port(self, worker):
    with self.semaphore:
      worker.run()