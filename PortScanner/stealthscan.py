import sys
import time
import socket
import platform
from threading import Semaphore, Thread
from random import randrange
from typing import Dict, List, Tuple
from .PacketBuild import PacketBuilder, TCP_FLAGS, CatchPacket

def current_time() -> float:
  return time.time() if platform.system().lower().startswith("linux") else time.process_time()

class StealthScan:
  """
  Object-oriented stealth TCP SYN scan.

  Attributes:
    target (str): hostname or IP to scan.
    port_range (Tuple[int, int]): (start, end) ports.
    timeout (float): socket timeout.
    threads (int): max concurrent threads.
    results (List[Tuple[int, str, str]]): list of (port, state, service).
  """
  def __init__(
    self,
    target: str,
    prange: str = '1-1024',
    timeout: float = 2.0,
    threads: int = 100
  ):
    self.target = target
    self.start_port, self.end_port = self._parse_port_range(prange)
    self.timeout = timeout
    self.max_threads = threads
    self.results: List[Tuple[int, str, str]] = []
    self.closed_count = 0

  def _parse_port_range(self, prange: str) -> Tuple[int, int]:
    # 'default' => well-known ports (1-1024)
    if prange == 'default':
      return (1, 1024)
    if '-' in prange:
      start, end = prange.split('-', 1)
      s, e = int(start), int(end)
      return (min(s, e), max(s, e))
    p = int(prange)
    return (p, p)

  def _resolve_host(self) -> str:
    try:
      return socket.gethostbyname(self.target)
    except Exception as e:
      print(f"[!] Failed to resolve {self.target}: {e}")
      sys.exit(1)

  def _get_our_addr(self) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      s.connect(("8.8.8.8", 80))
      return s.getsockname()[0]
    finally:
      s.close()

  def _worker(self, port: int, catcher: CatchPacket, sem: Semaphore):
    try:
      src_port = randrange(1025, 65535)
      builder = PacketBuilder(self.our_ip, self.target_ip)
      tcp_hdr = builder.build_tcp_header(src_port, port, TCP_FLAGS['syn'])
      ip_hdr = builder.build_ip_header(len(tcp_hdr), socket.IPPROTO_TCP)
      packet = ip_hdr + tcp_hdr

      sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
      sock.settimeout(self.timeout)
      sock.sendto(packet, (self.target_ip, port))
      pkt = catcher.next()
      if pkt:
        state = 'open'
        try:
          service = socket.getservbyport(port)
        except:
          service = ''
        self.results.append((port, state, service))
      else:
        self.closed_count += 1
    except KeyboardInterrupt:
      print('[-] Scan canceled by user')
      sys.exit(1)
    finally:
      sem.release()

  def scan(self) -> Dict[str, List[Tuple[int, str, str]]]:
    """
    Execute the stealth scan.

    Returns:
      dict with key 'scan' mapping to list of (port, state, service).
    """
    self.target_ip = self._resolve_host()
    self.our_ip = self._get_our_addr()
    catcher = CatchPacket(self.target_ip)._set_tcp()

    sem = Semaphore(self.max_threads)
    threads: List[Thread] = []
    start = current_time()

    for port in range(self.start_port, self.end_port + 1):
      sem.acquire()
      t = Thread(target=self._worker, args=(port, catcher, sem))
      t.daemon = True
      threads.append(t)
      t.start()

    for t in threads:
      t.join()

    elapsed = current_time() - start
    print(f"Scan completed in {elapsed:.2f}s; Closed/filtered: {self.closed_count}")
    return {'scan': sorted(self.results, key=lambda x: x[0])}