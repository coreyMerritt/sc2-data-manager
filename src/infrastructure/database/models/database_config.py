from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig():
  engine: str
  host: str
  name: str
  password: str
  port: int
  username: str
