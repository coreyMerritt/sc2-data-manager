from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserSIM:
  username: str
  password: str
  email_address: str
  user_type: str
  admin_secret: str | None
