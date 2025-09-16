#!/usr/bin/env python3
"""
Python3 UDP scanner module using PacketBuilder and default well-known ports.
Usage:
  from udpscan import ActiveUdpScan, format_results
  scan = ActiveUdpScan('example.com')
  results = scan.scan()
  print(format_results(results))
"""
import time
import socket
from threading import Thread, Semaphore, RLock
from random import randrange
from .PacketBuild import PacketBuilder, SocketHandler, CatchPacket

# Default well-known UDP ports
WELL_KNOWN_UDP_PORTS = [53, 69, 123, 161, 162, 500, 520, 1812, 1813, 5060]

def confirm_port_range(prange: str) -> list[int]:
  if prange == 'default':
    return WELL_KNOWN_UDP_PORTS
  parts = prange.split('-')
  if len(parts) == 2:
    start, end = map(int, parts)
    if start > end:
      start, end = end, start
    return list(range(start, end + 1))
  return [int(prange)]

def format_results(results: dict[str, list[tuple[int, str, str]]]) -> str:
  """
  Render scan results with aligned columns: Port, State, Service.
  """
  header = f"{'Port':<6} {'State':<13} Service"
  lines = [header, '-' * len(header)]
  for group in ('open', 'closed', 'filtered'):
    for port, state, service in sorted(results.get(group, [])):
      lines.append(f"{port:<6} {state:<13} {service}")
  return '\n'.join(lines)

class UdpScanner:
  def __init__(
      self,
      builder: PacketBuilder,
      send_sock: socket.socket,
      dip: str,
      sport: int,
      port: int,
      timeout: float
  ):
    self.builder = builder
    self.send_sock = send_sock
    self.dip = dip
    self.sport = sport
    self.port = port
    self.timeout = timeout

  def scan(self) -> tuple[int, str, str]:
    pkt = (
      self.builder.build_ip_header(payload_len=8, proto=socket.IPPROTO_UDP)
      + self.builder.build_udp_header(src_port=self.sport, dst_port=self.port)
    )
    self.send_sock.sendto(pkt, (self.dip, self.port))
    catcher = CatchPacket(self.dip)._set_icmp()
    start = time.time()
    while time.time() - start < self.timeout:
      data = catcher.next()
      if data:
        return (self.port, 'closed', 'icmp')
    return (self.port, 'open|filtered', 'none')

class ActiveUdpScan:
  def __init__(
      self,
      target: str,
      prange: str = 'default',
      timeout: float = 1.0,
      threads: int = 100
  ):
    self.target = target
    self.ports = confirm_port_range(prange)
    self.timeout = timeout
    self.threads = threads
    self.sock_handler = SocketHandler(timeout=self.timeout)
    # create raw UDP socket for sending
    self.send_sock = self.sock_handler.raw_socket(socket.IPPROTO_UDP)

  def scan(self) -> dict[str, list[tuple[int, str, str]]]:
    # resolve hostname to IP
    dip = socket.gethostbyname(self.target)
    sport = randrange(1024, 65535)
    # get source IP from send socket
    src_ip = self.send_sock.getsockname()[0]
    builder = PacketBuilder(src_ip=src_ip, dst_ip=dip)

    sem = Semaphore(self.threads)
    lock = RLock()
    results: dict[str, list[tuple[int, str, str]]] = {'open': [], 'closed': [], 'filtered': []}
    threads: list[Thread] = []

    def worker(port: int):
      with sem:
        p, state, service = UdpScanner(
          builder, self.send_sock, dip, sport, port, self.timeout
        ).scan()
        group = 'open' if state == 'open|filtered' else state
        with lock:
          results[group].append((p, state, service))

    for port in self.ports:
      t = Thread(target=worker, args=(port,))
      t.daemon = True
      threads.append(t)
      t.start()

    for t in threads:
      t.join()
    return results
