# -*- coding:utf-8 -*-

class Colors:
  RED    = '\033[91m'
  BLUE   = '\033[94m'
  YELLOW = '\033[93m'
  RESET  = '\033[0m'

class UrlRequestException(Exception):
  """
  Raised when an HTTP request to a URL fails.
  """
  def __init__(self, url: str = None, message: str = None):
    self.url = url
    default = f"Unable to request URL: {url}"
    super().__init__(message or default)

  def __str__(self):
    # Color the message red, then reset
    return f"{Colors.RED}{super().__str__()}{Colors.RESET}"
