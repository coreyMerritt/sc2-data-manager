from dataclasses import dataclass


@dataclass(frozen=True)
class AccountsConfig():
  admin_secret: str
