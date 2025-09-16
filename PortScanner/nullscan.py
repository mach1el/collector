import time
import socket
import random
from threading import Semaphore, Thread
from queue import Queue
from typing import Dict, List, Tuple, Optional

from .PacketBuild import PacketBuilder, CatchPacket

def current_time() -> float:
  """Return high-resolution monotonic time for measuring duration."""
  try:
    return time.perf_counter()
  except AttributeError:
    return time.time()

def parse_port_range(prange: str) -> Tuple[int, int]:
  """Parse a port or port-range string into (start_port, end_port).
     If prange=='default', use well-known ports 1-1024."""
  if prange == 'default':
    return 1, 1024
  if '-' in prange:
    start_str, end_str = prange.split('-', 1)
    start, end = int(start_str), int(end_str)
    if start > end:
      start, end = end, start
    return start, end
  port = int(prange)
  return port, port

def format_results(results: Dict[str, List[Tuple[int, str, str]]]) -> str:
  """
  Render scan results with aligned columns: Port, State, Service.
  """
  header = f"{'Port':<6} {'State':<13} Service"
  lines = [header, '-' * len(header)]
  for scans in results.values():
    for port, state, service in sorted(scans):
      lines.append(f"{port:<6} {state:<13} {service}")
  return '\n'.join(lines)

class NullScanner:
  """Perform null scans over a range of ports, defaulting to well-known ports if none specified."""

  def __init__(
    self,
    target: str,
    prange: Optional[str] = None,
    timeout: float = 1.0,
    threads: int = 100,
  ):
    self.dst_ip = socket.gethostbyname(target)
    self.start_port, self.end_port = parse_port_range(prange)
    self.timeout = timeout
    # PacketBuilder handles both packet creation and service lookup
    self.builder = PacketBuilder(
      src_ip=socket.gethostbyname(socket.gethostname()),
      dst_ip=self.dst_ip
    )
    self.sem = Semaphore(threads)
    self.open_q: Queue = Queue()
    self.closed_q: Queue = Queue()

  def _scan_port(self, port: int) -> None:
    """Scan a single port using the null-scan technique."""
    with self.sem:
      src_port = random.randrange(1024, 65535)
      flags = 0x00  # Null scan: no flags set
      tcp_hdr = self.builder.build_tcp_header(src_port, port, flags)
      ip_hdr = self.builder.build_ip_header(
        payload_len=len(tcp_hdr),
        proto=socket.IPPROTO_TCP,
      )
      packet = ip_hdr + tcp_hdr

      # Send via raw socket
      sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
      sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
      try:
        sock.sendto(packet, (self.dst_ip, port))
        time.sleep(self.timeout)
        # Sniff response
        sniffer = CatchPacket(self.dst_ip)._set_tcp()
        resp = sniffer.next()
        # Look up service; default to 'unknown' if not found
        try:
          service = sniffer.get_service(port)
        except Exception:
          service = 'unknown'
        if resp is None:
          self.open_q.put((port, 'open|filtered', service))
        else:
          self.closed_q.put((port, 'closed', service))
      finally:
        sock.close()

  def scan(self) -> Dict[str, List[Tuple[int, str, str]]]:
    """Execute the null scan and return raw results for formatting."""
    start = current_time()
    threads: List[Thread] = []
    for port in range(self.start_port, self.end_port + 1):
      t = Thread(target=self._scan_port, args=(port,))
      t.daemon = True
      threads.append(t)
      t.start()

    for t in threads:
      t.join()

    results: Dict[str, List[Tuple[int, str, str]]] = {self.dst_ip: []}
    while not self.open_q.empty():
      results[self.dst_ip].append(self.open_q.get())
    while not self.closed_q.empty():
      results[self.dst_ip].append(self.closed_q.get())

    elapsed = current_time() - start
    print(f"Null scan on {self.dst_ip} completed in {elapsed:.2f}s")
    return results