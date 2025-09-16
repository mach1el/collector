#! -*- coding:utf-8 -*-

try:
  import colorama
  from colorama import Fore, Style

  colorama.init()
except ImportError:
  class _Dummy:
    def __getattr__(self, name):
      return ""
  Fore = Style = _Dummy()  # type: ignore

from prettytable import PrettyTable

def coloured(text: str, colour: str) -> str:
  """
  Wraps `text` in ANSI color codes (via colorama).
  Supported colours: red, green, yellow, blue, cyan, magenta.
  """
  mapping = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "cyan": Fore.CYAN,
    "magenta": Fore.MAGENTA,
  }
  return f"{mapping.get(colour, '')}{text}{Style.RESET_ALL}"

def print_color(text: str, colour: str, end: str = "\n") -> None:
  """
  Prints `text` to stdout in the given colour.
  Falls back to plain text if colorama isn’t available.
  """
  msg = coloured(text, colour)
  print(msg, end=end)

def format_results(results: dict[str, list[tuple[int, str, str]]]) -> str:
  """
  Render scan results with aligned columns: Port, State, Service.
  """
  # Header
  header = f"{'Port':<6} {'State':<13} Service"
  lines = [header, '-' * len(header)]
  # Rows
  for scans in results.values():
    for port, state, service in sorted(scans):
      lines.append(f"{port:<6} {state:<13} {service}")
  return '\n'.join(lines)