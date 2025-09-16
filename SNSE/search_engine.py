import re
import sys
import time
import random
import threading
from abc import ABC, abstractmethod
from html import unescape
import requests
from utils import print_color

class Parser:
  """
  Clean HTML and extract patterns using regex.
  """
  TAG_RE = re.compile(r'<[^>]+>')

  @staticmethod
  def clean(html: str) -> str:
    """Remove HTML tags, unescape entities, and normalize whitespace."""
    text = Parser.TAG_RE.sub('', html)
    text = unescape(text)
    text = re.sub(r'%2[fF]', '/', text)
    text = re.sub(r'%3[aA]', ':', text)
    return re.sub(r'\s+', ' ', text).strip()

class SkipValue:
  def __init__(self):
    self._seen = set()
  def skip(self, item):
    self._seen.add(item)
  def items(self):
    return list(self._seen)

class Counter:
  def __init__(self):
    self._counts = {}
  def increment(self, key):
    self._counts[key] = self._counts.get(key, 0) + 1
  def list(self):
    return sorted(self._counts, key=self._counts.get, reverse=True)

class BaseSearcher(ABC):
  STEP = 100
  MAX_RESULTS = 600
  MIN_DELAY = 1
  MAX_DELAY = 3

  def __init__(self, domain, user_agent=None, user_agents=None):
    self.domain = domain
    self.engine = 'google'
    self.session = requests.Session()
    # Setup UA list
    if user_agents:
      self.user_agents = user_agents
    elif user_agent:
      self.user_agents = [user_agent]
    else:
      self.user_agents = [
        'Mozilla/5.0 (compatible; SNSE/1.0; +https://github.com/username/SNSE)',
      ]
    self.skipper = SkipValue()
    self.counter = Counter()
    self.results = []
    self.domain = domain
    self.session = requests.Session()
    # Setup UA list
    if user_agents:
      self.user_agents = user_agents
    elif user_agent:
      self.user_agents = [user_agent]
    else:
      self.user_agents = [
        'Mozilla/5.0 (compatible; SNSE/1.0; +https://github.com/username/SNSE)',
      ]
    self.skipper = SkipValue()
    self.counter = Counter()
    self.results = []

  @abstractmethod
  def _build_query_url(self, start: int) -> str:
    pass

  @abstractmethod
  def _extract(self, text: str) -> list:
    pass

  def _fetch(self, url: str) -> str:
    ua = random.choice(self.user_agents)
    self.session.headers.update({'User-Agent': ua})
    try:
      resp = self.session.get(url, timeout=10)
      if resp.status_code == 429:
        print_color(f'429 Too Many Requests for {url}, retrying after backoff...', 'yellow')
        time.sleep(5)
        resp = self.session.get(url, timeout=10)
      resp.raise_for_status()
      return resp.text
    except requests.RequestException as e:
      print_color(f'HTTP error on {url}: {e}', 'red')
      return ''

  def process(self):
    for start in range(0, self.MAX_RESULTS, self.STEP):
      print_color(f'{self.__class__.__name__}: fetching results {start}-{start + self.STEP}', 'green')
      raw = self._fetch(self._build_query_url(start))
      if raw:
        clean = Parser.clean(raw)
        items = self._extract(clean)
        for item in items:
          self.counter.increment(item)
      delay = random.uniform(self.MIN_DELAY, self.MAX_DELAY)
      time.sleep(delay)
    for item in self.counter.list():
      self.skipper.skip(item)
    self.results = self.skipper.items()

  def print_results(self):
    for url in self.results:
      print_color(url, 'cyan')

class TwitterSearcher(BaseSearcher):
  def _build_query_url(self, start):
    q = f'site:twitter.com "{self.domain}"'
    return f'https://www.google.com/search?num={self.STEP}&start={start}&q={requests.utils.quote(q)}'
  def _extract(self, text: str) -> list:
    return re.findall(r'https?://twitter\.com/([A-Za-z0-9_]+)', text)

class LinkedInSearcher(BaseSearcher):
  def _build_query_url(self, start):
    q = f'site:linkedin.com/in "{self.domain}"'
    return f'https://www.google.com/search?num={self.STEP}&start={start}&q={requests.utils.quote(q)}'
  def _extract(self, text: str) -> list:
    return re.findall(r'https?://www\.linkedin\.com/in/([A-Za-z0-9\-]+)', text)

class EmailSearcher(BaseSearcher):
  def _build_query_url(self, start):
    q = f'@{self.domain}'
    return f'https://www.google.com/search?num={self.STEP}&start={start}&q={requests.utils.quote(q)}'
  def _extract(self, text: str) -> list:
    pattern = rf'[\w\.-]+@{re.escape(self.domain)}'
    return re.findall(pattern, text)

class FacebookSearcher(BaseSearcher):
  def _build_query_url(self, start):
    q = f'site:facebook.com "{self.domain}"'
    return f'https://www.google.com/search?num={self.STEP}&start={start}&q={requests.utils.quote(q)}'
  def _extract(self, text: str) -> list:
    return re.findall(r'https?://www\.facebook\.com/([A-Za-z0-9\.]+)', text)

class InstagramSearcher(BaseSearcher):
  def _build_query_url(self, start):
    q = f'site:instagram.com "{self.domain}"'
    return f'https://www.google.com/search?num={self.STEP}&start={start}&q={requests.utils.quote(q)}'
  def _extract(self, text: str) -> list:
    return re.findall(r'https?://www\.instagram\.com/([A-Za-z0-9_\.]+)', text)

class TikTokSearcher(BaseSearcher):
  def _build_query_url(self, start):
    q = f'site:tiktok.com/@"{self.domain}"'
    return f'https://www.google.com/search?num={self.STEP}&start={start}&q={requests.utils.quote(q)}'
  def _extract(self, text: str) -> list:
    return re.findall(r'https?://www\.tiktok\.com/@([A-Za-z0-9_\.]+)', text)

class GitHubSearcher(BaseSearcher):
  def _build_query_url(self, start):
    q = f'site:github.com "{self.domain}"'
    return f'https://www.google.com/search?num={self.STEP}&start={start}&q={requests.utils.quote(q)}'
  def _extract(self, text: str) -> list:
    return re.findall(r'https?://github\.com/([A-Za-z0-9\-]+)', text)

def run_all(domain, user_agent=None, user_agents=None, engine='google'):
  """
  domain: search target (domain or name)
  engine: 'google' or 'bing'
  """
  ualist = [user_agent] if user_agent else None
  searchers = [
    TwitterSearcher,
    LinkedInSearcher,
    EmailSearcher,
    FacebookSearcher,
    InstagramSearcher,
    TikTokSearcher,
    GitHubSearcher
  ]
  threads = []
  for cls in searchers:
    # pass engine to each searcher
    obj = cls(domain, user_agent, user_agents=ualist)
    obj.engine = engine
    t = threading.Thread(target=lambda s=obj: (s.process(), s.print_results()))
    t.start()
    threads.append(t)
  for t in threads:
    t.join()
  ualist = [user_agent] if user_agent else None
  searchers = [
    TwitterSearcher,
    LinkedInSearcher,
    EmailSearcher,
    FacebookSearcher,
    InstagramSearcher,
    TikTokSearcher,
    GitHubSearcher
  ]
  threads = []
  for cls in searchers:
    obj = cls(domain, user_agent, user_agents=ualist)
    t = threading.Thread(target=lambda s=obj: (s.process(), s.print_results()))
    t.start()
    threads.append(t)
  for t in threads:
    t.join()