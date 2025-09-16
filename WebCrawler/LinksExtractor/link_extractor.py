#! -*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

class LinkExtractor:
  """
  Fetches pages for one or more base URLs, extracts all <a href=""> links,
  normalizes them (removes scheme + www), and returns a set of unique paths.
  """

  _abs_pattern = re.compile(r'^(https?|ftp)://', re.IGNORECASE)

  def __init__(self, base_urls, max_workers=5, timeout=5):
    if isinstance(base_urls, str):
      base_urls = [base_urls]
    self.base_urls = base_urls
    self.max_workers = max_workers
    self.timeout = timeout
    self.session = requests.Session()

  def _fetch(self, url):
    try:
      r = self.session.get(url, timeout=self.timeout)
      r.raise_for_status()
      return url, r.text
    except Exception:
      return url, None

  def _parse_links(self, base_url, html):
    soup = BeautifulSoup(html, 'html.parser')
    found = set()

    # relative URLs
    for a in soup.find_all('a', href=True):
      href = a['href'].strip()
      # build absolute URL for relative hrefs
      if not self._abs_pattern.match(href):
        href = urljoin(base_url, href)
      found.add(href)

    return found

  def _normalize(self, url):
    p = urlparse(url)
    # drop scheme, www., lower-case host
    host = p.netloc.lower().lstrip('www.')
    path = p.path.rstrip('/')
    qs = f"?{p.query}" if p.query else ""
    return host + path + qs

  def extract(self):
    """
    Returns a sorted list of unique, normalized link strings
    gathered from all base URLs.
    """
    links = set()

    with ThreadPoolExecutor(max_workers=self.max_workers) as exe:
      futures = [exe.submit(self._fetch, u) for u in self.base_urls]
      for future in as_completed(futures):
        url, html = future.result()
        if html:
          raw_links = self._parse_links(url, html)
          for raw in raw_links:
            links.add(self._normalize(raw))

    return sorted(links)