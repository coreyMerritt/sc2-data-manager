from dataclasses import dataclass


@dataclass(frozen=True)
class TokenHasherConfig():
  secret: str
