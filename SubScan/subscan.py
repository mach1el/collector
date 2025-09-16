import sys
from socket import gethostbyname, gethostbyname_ex
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from prettytable import PrettyTable
from .wordlist import mydict

# Cache DNS lookups to minimize resolution overhead
@lru_cache(maxsize=None)
def resolve(host):
  try:
    name, aliases, ipaddrs = gethostbyname_ex(host)
    seen = set([host] + aliases + ipaddrs)
    return list(seen)
  except:
    return []

class SubdomainScanner:
  def __init__(self, host, wordlist=mydict, threads=10, output=None, verbose=False):
    self.host = host
    self.wordset = set(wordlist)
    self.threads = threads
    self.output = output
    self.verbose = verbose
    self.targets = [host] + [f"{w}.{host}" for w in self.wordset]
    self.total = len(self.targets)
    self.subdomains = []
    self.subcount = 0
    self.done = 0
    self.count_lock = Lock()

  def scan(self, sub):
    results = []
    for entry in resolve(sub):
      try:
        ip = gethostbyname(entry)
      except:
        continue
      results.append((ip, entry))
      # Count if prefix matches
      if entry.split('.')[0] in self.wordset:
        with self.count_lock:
          self.subcount += 1
    return results

  def run(self):
    # Progress bar only
    def print_progress():
      self.done += 1
      pct = self.done / self.total * 100
      sys.stderr.write(f"\rProgress: {pct:.1f}% ({self.done}/{self.total})")
      sys.stderr.flush()

    with ThreadPoolExecutor(max_workers=self.threads) as executor:
      futures = {executor.submit(self.scan, t): t for t in self.targets}
      for fut in as_completed(futures):
        self.subdomains.extend(fut.result())
        if self.verbose:
          print_progress()
    if self.verbose:
      sys.stderr.write("\n")

    # Output results
    table = PrettyTable(['IP', 'Hostname'])
    for ip, entry in self.subdomains:
      table.add_row([ip, entry])
    print(table)

    # Write to file if specified
    if self.output:
      with open(self.output, 'w') as f:
        for ip, entry in self.subdomains:
          f.write(f"{ip}\t{entry}\n")

    print(f"[*] Completed. Found {self.subcount} matching subdomains under {self.host}.")