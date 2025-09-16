# -*- coding:utf-8 -*-

import requests
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor, as_completed

class UrlAvailabilityChecker:
  """
  Checks if a URL is reachable over HTTP and HTTPS.
  """

  def __init__(self, url, timeout=5):
    self.url = url.rstrip('/')
    self.timeout = timeout
    self.session = requests.Session()

  def check(self):
    results = {}
    for scheme in ('http', 'https'):
      full = f"{scheme}://{self.url}"
      try:
        resp = self.session.head(full, timeout=self.timeout)
        results[scheme] = (resp.status_code, resp.reason)
      except RequestException as e:
        results[scheme] = (None, str(e))
    return results

class HttpMethodTester:
  """
  Sends a variety of HTTP methods to a target URL and reports status.
  """

  METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'PATCH']

  def __init__(self, base_url, headers=None, timeout=5, max_workers=4):
    self.base_url = base_url.rstrip('/')
    self.session = requests.Session()
    self.headers = headers or {}
    self.timeout = timeout
    self.max_workers = max_workers

  def _send(self, method):
    try:
      resp = self.session.request(
        method, self.base_url, headers=self.headers, timeout=self.timeout
      )
      return method, resp.status_code, resp.reason
    except RequestException as e:
      return method, None, str(e)

  def run_all(self):
    """
    Tests all supported methods concurrently.
    Returns a dict: { method: (status_code, reason) }
    """
    results = {}
    with ThreadPoolExecutor(max_workers=self.max_workers) as exe:
      futures = { exe.submit(self._send, m): m for m in self.METHODS }
      for fut in as_completed(futures):
        method, code, reason = fut.result()
        results[method] = (code, reason)
    return results

  def report(self, results):
    """
    Prints a color-coded summary of results.
    """
    from termcolor import colored, cprint

    for method, (code, reason) in results.items():
      if code is None:
        cprint(f"{method}: Failed ({reason})", 'red')
      elif 100 <= code < 200:
        cprint(f"{method}: {code} {reason}", 'blue')
      elif 200 <= code < 300:
        cprint(f"{method}: {code} {reason}", 'green')
      elif 300 <= code < 400:
        cprint(f"{method}: {code} {reason}", 'yellow')
      else:
        cprint(f"{method}: {code} {reason}", 'red')
