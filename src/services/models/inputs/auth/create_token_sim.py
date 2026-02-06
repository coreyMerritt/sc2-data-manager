from dataclasses import dataclass


@dataclass(frozen=True)
class CreateTokenSIM:
  username: str
  password: str
