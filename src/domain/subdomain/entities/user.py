from datetime import UTC, datetime

import ulid as ULID

from domain.enums.user_type import UserType
from domain.exceptions.validation_err import ValidationErr


class User:
  _ulid: str
  _username: str
  _email_address: str
  _password_hash: str
  _user_type: UserType
  _email_verified: bool
  _created_at: datetime
  _disabled_at: datetime | None

  def __init__(
    self,
    username: str,
    email_address: str,
    password_hash: str,
    user_type: UserType,
    ulid: str | None,
    email_verified: bool | None,
    created_at: datetime | None,
    disabled_at: datetime | None
  ):
    self.username = username
    self.email_address = email_address
    self.password_hash = password_hash
    self.user_type = user_type
    self.ulid = str(ULID.new())
    if ulid:
      self.ulid = ulid
    self.email_verified = False
    if email_verified:
      self.email_verified = email_verified
    self.created_at = datetime.now(tz=UTC)
    if created_at:
      self.created_at = created_at
    self.disabled_at = None
    if disabled_at:
      self.disabled_at = disabled_at
    self._validate_properties()

  @property
  def ulid(self) -> str:
    return self._ulid

  @ulid.setter
  def ulid(self, ulid: str) -> None:
    self._ulid = ulid

  @property
  def username(self) -> str:
    return self._username

  @username.setter
  def username(self, username: str) -> None:
    self._username = username

  @property
  def email_address(self) -> str:
    return self._email_address

  @email_address.setter
  def email_address(self, email_address: str) -> None:
    self._email_address = email_address

  @property
  def user_type(self) -> UserType:
    return self._user_type

  @user_type.setter
  def user_type(self, user_type: UserType) -> None:
    self._user_type = user_type

  @property
  def password_hash(self) -> str:
    return self._password_hash

  @password_hash.setter
  def password_hash(self, password_hash: str) -> None:
    self._password_hash = password_hash

  @property
  def email_verified(self) -> bool:
    return self._email_verified

  @email_verified.setter
  def email_verified(self, email_verified: bool) -> None:
    self._email_verified = email_verified

  @property
  def created_at(self) -> datetime:
    return self._created_at

  @created_at.setter
  def created_at(self, created_at: datetime) -> None:
    self._created_at = created_at

  @property
  def disabled_at(self) -> datetime | None:
    return self._disabled_at

  @disabled_at.setter
  def disabled_at(self, disabled_at: datetime | None) -> None:
    self._disabled_at = disabled_at

  def enable(self) -> None:
    if self.disabled_at is not None:
      self.disabled_at = None

  def disable(self) -> None:
    if self.disabled_at is None:
      self.disabled_at = datetime.now(UTC)

  def __eq__(self, other):
    return isinstance(other, User) and self.ulid == other.ulid

  def _validate_properties(self) -> None:
    try:
      assert isinstance(self.ulid, str), "ulid"
      assert isinstance(self.username, str), "username"
      assert self.username.strip(), "username"
      assert isinstance(self.email_address, str), "email_address"
      assert "@" in self.email_address, "email_address"
      assert isinstance(self.password_hash, str), "password_hash"
      assert isinstance(self.email_verified, bool), "email_verified"
      assert isinstance(self.created_at, datetime), "created_at"
      assert (
        self.disabled_at is None
        or isinstance(self.disabled_at, datetime)
      ), "disabled_at"
    except AssertionError as e:
      raise ValidationErr(attribute_name=str(e)) from e
