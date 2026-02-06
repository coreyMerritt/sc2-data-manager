from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateUserSIM:
  ulid: str
  username: str
  email_address: str
  email_verified: bool
  disabled: bool
  user_type: str
  admin_secret: str | None
