import time
import socket
from random import randrange
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from .PacketBuild import PacketBuilder, TCP_FLAGS, CatchPacket

def get_local_ip() -> str:
  """Get the local host IP."""
  return socket.gethostbyname(socket.gethostname())

class XmasScan:
  """Perform a single Xmas scan on a target port."""

  def __init__(self, sock, target_ip: str, port: int, timeout: float, catcher: CatchPacket, results_queue: Queue):
    self.sock = sock
    self.target_ip = target_ip
    self.port = port
    self.timeout = timeout
    self.catcher = catcher
    self.results = results_queue

  def scan(self):
    src_ip = get_local_ip()
    src_port = randrange(1024, 65535)
    builder = PacketBuilder(src_ip, self.target_ip)
    flags = TCP_FLAGS['xmas']
    tcp_hdr = builder.build_tcp_header(src_port, self.port, flags)
    ip_hdr = builder.build_ip_header(len(tcp_hdr), socket.IPPROTO_TCP)
    packet = ip_hdr + tcp_hdr

    try:
      self.sock.sendto(packet, (self.target_ip, 0))
      time.sleep(self.timeout)
      resp = self.catcher.next()
      state = 'closed' if resp else 'open|filtered'
      service = self.catcher.get_service(self.port)
      self.results.put((self.port, state, service))
    except Exception:
      pass

class ActiveXmas:
  """Manage Xmas scan over a range of ports."""
  WELL_KNOWN = range(1, 1025)

  def __init__(self, target: str, prange: str = 'default', timeout: float = 0.3, threads: int = 100):
    self.target_ip = socket.gethostbyname(target)
    self.prange = self._parse_range(prange)
    self.timeout = timeout
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    self.sock.settimeout(timeout)
    self.catcher = CatchPacket(self.target_ip)._set_tcp()
    self.results = Queue()
    self.threads = threads

  def _parse_range(self, prange: str):
    if prange == 'default':
      return ActiveXmas.WELL_KNOWN
    if '-' in prange:
      start, end = prange.split('-', 1)
      return range(int(start), int(end) + 1)
    return [int(prange)]

  def scan(self) -> dict[str, list[tuple[int, str, str]]]:
    """Execute the Xmas scan and return a results dict."""
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=self.threads) as pool:
      futures = [
        pool.submit(
          XmasScan(
            sock=self.sock,
            target_ip=self.target_ip,
            port=port,
            timeout=self.timeout,
            catcher=self.catcher,
            results_queue=self.results
          ).scan
        ) for port in self.prange
      ]
      for _ in as_completed(futures): pass

    scanned = []
    while not self.results.empty():
      scanned.append(self.results.get())

    # return only dict; drop elapsed
    return {self.target_ip: scanned}