class DomainHandler:
  _BYPASS = {
    'edu', 'com', 'biz', 'net', 'org', 'info', 'co', 'gov', 'mil',
    'name', 'tel', 'web', 'tv', 'int', 'ac', 'gob', 'ed', 'av', 'dr',
    'gen', 'nom', 'sld'
  }

  def __init__(self, domain: str):
    self.original = domain.strip()
    self.domain = self._clean(self.original)

  def _clean(self, domain: str) -> str:
    parts = domain.lower().split('.')
    if len(parts) == 3 and parts[1] in self._BYPASS:
      return '.'.join([parts[0], parts[2]])
    return domain

  def get(self) -> str:
    return self.domain