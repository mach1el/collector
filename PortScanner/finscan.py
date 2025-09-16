"""
finscan.py

Object-Oriented FIN Scan module to be used in Collector.
Define `FinScanner` class for FIN scan logic.
"""
import ipaddress
import socket
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from .PacketBuild import PacketBuilder, TCP_FLAGS

class FinScanner:
  """
  Perform TCP FIN scans on given targets.

  Attributes:
    targets (list[str]): hostnames, IPs, or CIDRs.
    prange (str): e.g. 'default', '1-1024', '80,443'.
    timeout (float): timeout per port.
    threads (int): max concurrent threads.
    results (dict[str, list[tuple[int, str, str]]]): scan results mapping IP to list of (port, state, service).
  """
  WELL_KNOWN_RANGE = (1, 1024)

  def __init__(self, targets: str | list[str], prange: str, timeout: float = 1.0, threads: int = 10):
    self.targets = [targets] if isinstance(targets, str) else list(targets)
    self.prange = prange
    self.timeout = timeout
    self.threads = threads
    self.results: dict[str, list[tuple[int, str, str]]] = {}

  def _resolve_host(self, target: str) -> str:
    try:
      ipaddress.ip_address(target)
      return target
    except ValueError:
      return socket.gethostbyname(target)

  def _get_local_ip(self, remote_ip: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
      try:
        s.connect((remote_ip, 1))
        return s.getsockname()[0]
      except Exception:
        return '0.0.0.0'

  def _parse_ports(self) -> list[int]:
    if self.prange.lower() == 'default':
      start, end = self.WELL_KNOWN_RANGE
      return list(range(start, end + 1))
    ports: list[int] = []
    for part in self.prange.split(','):
      if '-' in part:
        a, b = map(int, part.split('-'))
        ports.extend(range(a, b + 1))
      else:
        ports.append(int(part))
    return ports

  def _fin_scan_port(self, builder: PacketBuilder, ip: str, port: int) -> tuple[int, str, str]:
    # Build FIN packet with random source port
    src_port = random.randrange(1024, 65535)
    packet = (
      builder.build_ip_header(payload_len=20, proto=socket.IPPROTO_TCP)
      + builder.build_tcp_header(
          src_port=src_port,
          dst_port=port,
          flags=TCP_FLAGS['fin'],
      )
    )
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    sock.settimeout(self.timeout)
    try:
      sock.sendto(packet, (ip, 0))
      resp, _ = sock.recvfrom(65535)
      flags = resp[33]
      state = 'closed' if (flags & 0x04) else 'open|filtered'
    except socket.timeout:
      state = 'open|filtered'
    except Exception:
      state = 'open|filtered'
    finally:
      sock.close()

    try:
      service = socket.getservbyport(port, 'tcp')
    except OSError:
      service = ''

    return port, state, service

  def scan(self) -> dict[str, list[tuple[int, str, str]]]:
    """
    Execute FIN scan across all targets and ports.
    Returns dict mapping IP to list of (port, state, service).
    """
    ip_list: list[str] = []
    for tgt in self.targets:
      if '/' in tgt:
        try:
          net = ipaddress.ip_network(tgt, strict=False)
          ip_list.extend(str(ip) for ip in net.hosts())
        except ValueError:
          raise ValueError(f"Invalid CIDR network: {tgt}")
      else:
        try:
          ip = self._resolve_host(tgt)
        except Exception:
          continue
        ip_list.append(ip)

    ports = self._parse_ports()
    for ip in ip_list:
      self.results[ip] = []
      src_ip = self._get_local_ip(ip)
      builder = PacketBuilder(src_ip, ip)
      with ThreadPoolExecutor(max_workers=self.threads) as executor:
        futures = {executor.submit(self._fin_scan_port, builder, ip, p): p for p in ports}
        for future in as_completed(futures):
          port, state, service = future.result()
          self.results[ip].append((port, state, service))

    return self.results