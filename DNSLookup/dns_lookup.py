from socket import gethostbyname
from dns import resolver, reversename, zone, query
from utils import print_color

SUPPORTED_TYPES = [
  "A", "AAAA", "CNAME", "MX", "NS", "PTR", "SOA", "TXT", "SRV", "ANY"
]


def reverse_lookup(ip_address):
  """
  Perform a PTR (reverse) lookup for the given IP address.

  Returns the hostname or None if lookup fails.
  """
  try:
    rev_name = reversename.from_address(ip_address)
    answers = resolver.resolve(rev_name, 'PTR')
    return str(answers[0]).rstrip('.')
  except Exception:
    return None


def format_rrset(name, rtype, records):
  """
  Format and print DNS records for a given RR type with colors.
  """
  header = f"[*] {rtype} records for {name}:"
  print_color(header, 'blue')
  for record in records:
    text = record.rstrip('.')
    print_color(f"  - {text}", "green")


def query_records(name, record_types=None):
  """
  Query forward DNS records for 'name'. If record_types is None, uses SUPPORTED_TYPES.

  Prints results directly and returns None.
  """
  types = record_types or SUPPORTED_TYPES
  for rtype in types:
    try:
      answers = resolver.resolve(name, rtype, tcp=True)
      records = [r.to_text() for r in answers]
      format_rrset(name, rtype, records)
    except resolver.NoAnswer:
      continue
    except resolver.NXDOMAIN:
      print_color(f"Domain {name} does not exist.", 'red')
      break
    except Exception as e:
      print_color(f"[!] Error fetching {rtype} for {name}: {e}", "yellow")

def dns_lookup(name, record_types=None):
  """
  Perform forward and reverse lookups for the given domain or hostname.

  Uses print for all output.
  """
  # Forward lookup
  print()
  query_records(name, record_types)

  # IPv4 reverse lookup
  try:
    ip4 = gethostbyname(name)
    host4 = reverse_lookup(ip4)
    if host4:
      print()
      query_records(host4, record_types)
  except Exception:
      pass

  # IPv6 reverse lookup
  try:
    answers = resolver.resolve(name, 'AAAA')
    for rr in answers:
      ip6 = rr.address
      host6 = reverse_lookup(ip6)
      if host6:
        print()
        query_records(host6, record_types)
  except Exception:
      pass

def attempt_zone_transfer(domain):
  """
  Attempt DNS zone transfer (AXFR) on all NS records of the domain.

  Prints discovered hostnames.
  """
  discovered = False
  try:
    ns_list = resolver.resolve(domain, 'NS')
    for ns in ns_list:
      ns_name = str(ns.target).rstrip('.')
      try:
        z = zone.from_xfr(query.xfr(ns_name, domain))
        for node_name, node in z.nodes.items():
          for rdataset in node.rdatasets:
            label = node_name.to_text()
            if label not in ('@', '*'):
              print_color(f"{label}.{domain}", 'cyan')
              discovered = True
      except Exception:
            continue
  except Exception:
    pass

  if not discovered:
    print_color('Zone transfer not available.', 'red')

class DNSCollector:
  """
  High-level interface for DNS lookups and zone transfers.
  """
  def __init__(self, target, record_types=None):
    """
    :param target: Domain or hostname to query.
    :param record_types: List of DNS record types to lookup (default: all SUPPORTED_TYPES).
    """
    self.target = target
    self.record_types = record_types

  def lookup(self):
    """
    Perform forward and reverse DNS lookups on the target.
    """
    dns_lookup(self.target, self.record_types)

  def zone_transfer(self):
    """
    Attempt DNS zone transfer on the target.
    """
    attempt_zone_transfer(self.target)
