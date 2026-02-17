from datetime import datetime, timezone

from sqlmodel import select

from domain.interfaces.authenticator import AuthenticatorInterface
from infrastructure.auth.exceptions.token_expired_err import TokenExpiredErr
from infrastructure.auth.exceptions.token_not_found_err import TokenNotFoundErr
from infrastructure.auth.exceptions.token_revoked_err import TokenRevokedErr
from infrastructure.auth.token_hasher import TokenHasher
from infrastructure.database.database import Database
from infrastructure.database.orm.auth_token_orm import AuthTokenORM


class Authenticator(AuthenticatorInterface):
  _database: Database
  _token_hasher: TokenHasher

  def __init__(self, database: Database, token_hasher: TokenHasher):
    self._token_hasher = token_hasher
    self._database = database

  def authenticate(self, token: str) -> str:
    token_hash = self._token_hasher.hash(token)
    with self._database.get_session() as session:
      statement = (
        select(AuthTokenORM)
        .where(AuthTokenORM.token_hash == token_hash)
      )
      auth_token = session.exec(statement).one_or_none()
    if auth_token is None:
      raise TokenNotFoundErr()
    if auth_token.revoked_at is not None:
      raise TokenRevokedErr()
    if (
      auth_token.expires_at is not None
      and auth_token.expires_at < datetime.now(tz=timezone.utc)
    ):
      raise TokenExpiredErr()
    return auth_token.user_ulid
