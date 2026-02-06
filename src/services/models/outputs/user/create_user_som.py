from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserSOM:
  ulid: str
  email_address: str
  username: str
  password_hash: str
  user_type: str
