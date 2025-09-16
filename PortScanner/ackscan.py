# -*- coding: utf-8 -*-

import sys
import time
import socket
from threading import Semaphore, Thread
from queue import Queue
from random import randrange
from .PacketBuild import PacketBuilder, TCP_FLAGS, SocketHandler, CatchPacket

# Thread-safe queues
_g_filtered = Queue()
_g_unfiltered = Queue()

def current_time():
  return time.time()

def parse_port_range(prange):
  if '-' in prange:
    start, end = map(int, prange.split('-', 1))
    if start > end:
      start, end = end, start
    return range(start, end + 1)
  return [int(prange)]

class AckScanWorker:
  """Per-port ACK probe."""
  def __init__(self, sock, builder, catcher, target_ip, port):
    self.sock = sock
    self.builder = builder
    self.catcher = catcher
    self.target_ip = target_ip
    self.port = port

  def run(self):
    try:
      # build headers
      ip_hdr = self.builder.build_ip_header(20, socket.IPPROTO_TCP)
      tcp_hdr = self.builder.build_tcp_header(randrange(1024, 65535),
                                              self.port,
                                              TCP_FLAGS['ack'])
      pkt = ip_hdr + tcp_hdr

      # send and listen
      self.sock.sendto(pkt, (self.target_ip, 0))
      time.sleep(0.05)
      resp = self.catcher.next()
      service = self.catcher.get_service(self.port)

      if resp is None:
        # no reply -> filtered/open|filtered
        _g_filtered.put((self.port, 'filtered', service))
      else:
        data = resp[0]  # raw packet
        flags = data[33] if isinstance(data[33], int) else ord(data[33])
        if flags & TCP_FLAGS['rst']:
          _g_unfiltered.put((self.port, 'unfiltered', service))
        else:
          _g_filtered.put((self.port, 'filtered', service))
    except KeyboardInterrupt:
      sys.exit(1)


class ActiveAckScanner:
  """Manages threading and returns structured results."""
  def __init__(self, target, prange, timeout, threads=10):
    # resolve IP once
    self.target_ip = socket.gethostbyname(target)
    self.ports = parse_port_range(prange)
    self.timeout = float(timeout)

    handler = SocketHandler(self.timeout)
    # raw socket for TCP probes
    self.sock = handler.raw_socket(socket.IPPROTO_TCP)
    # determine local IP
    tmp = handler.connect_socket('8.8.8.8', 53)
    src_ip = tmp.getsockname()[0] if tmp else '0.0.0.0'
    # packet builder & catcher use target_ip
    self.builder = PacketBuilder(src_ip, self.target_ip)
    self.catcher = CatchPacket(self.target_ip)._set_tcp()

    self.semaphore = Semaphore(threads)

  def scan(self) -> dict[str, list[tuple[int, str, str]]]:
    start = current_time()
    threads = []

    for port in self.ports:
      worker = AckScanWorker(self.sock,
                             self.builder,
                             self.catcher,
                             self.target_ip,
                             port)
      t = Thread(target=self._scan_port, args=(worker,))
      t.daemon = True
      threads.append(t)
      t.start()

    for t in threads:
      t.join()

    # collect
    filtered, unfiltered = [], []
    while not _g_filtered.empty():
      filtered.append(_g_filtered.get())
    while not _g_unfiltered.empty():
      unfiltered.append(_g_unfiltered.get())

    # combine both lists
    all_results = filtered + unfiltered

    # You could group by state if desired, but for format_results just wrap in one dict
    return {'default': all_results}

  def _scan_port(self, worker):
    with self.semaphore:
      worker.run()