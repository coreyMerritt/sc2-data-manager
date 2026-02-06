from datetime import datetime, timezone
from typing import ClassVar, Optional

from sqlmodel import Field, SQLModel


class UserORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "user"
  ulid: str = Field(primary_key=True, max_length=26)
  username: str = Field(
    nullable=False,
    unique=True,
    index=True,
    max_length=64
  )
  email_address: str = Field(
    nullable=False,
    unique=True,
    index=True,
    max_length=255
  )
  password_hash: str = Field(
    nullable=False,
    max_length=255,
  )
  user_type: str = Field(
    nullable=False,
    max_length=255,
  )
  email_verified: bool = Field(nullable=False)
  created_at: datetime = Field(
    default_factory=lambda: datetime.now(tz=timezone.utc),
    nullable=False
  )
  disabled_at: Optional[datetime] = Field(default=None)
