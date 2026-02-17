from datetime import datetime, timezone
from typing import ClassVar

import ulid
from sqlmodel import Column, DateTime, Field, SQLModel


def generate_ulid() -> str:
  return ulid.new().str


class AuthTokenORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "auth_token"
  ulid: str = Field(
    default_factory=generate_ulid,
    primary_key=True,
    max_length=26,
  )
  user_ulid: str = Field(
    foreign_key="user.ulid",
    nullable=False,
    max_length=26,
  )
  token_hash: str = Field(
    nullable=False,
    max_length=255,
  )
  expires_at: datetime | None = Field(
    sa_column=Column(DateTime(timezone=True)),
    default=None
  )
  revoked_at: datetime | None = Field(
    sa_column=Column(DateTime(timezone=True)),
    default=None
  )
  created_at: datetime = Field(
    default_factory=lambda: datetime.now(tz=timezone.utc),
    nullable=False,
  )
