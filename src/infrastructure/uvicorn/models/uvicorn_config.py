from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class UvicornConfig():
  access_log: bool
  app: str
  factory: bool
  host: str
  log_config: str
  port: int
  reload: bool
  reload_excludes: List[str]
  server_header: bool
