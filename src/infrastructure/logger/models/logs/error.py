from dataclasses import dataclass


@dataclass
class Error:
  name: str
  message: str
  stack: str
