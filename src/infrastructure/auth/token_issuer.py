import secrets
from datetime import datetime, timedelta, timezone

from infrastructure.auth.models.token_issuer_config import TokenIssuerConfig
from infrastructure.auth.token_hasher import TokenHasher
from infrastructure.database.database import Database
from infrastructure.database.orm.auth_token_orm import AuthTokenORM


class TokenIssuer:
  _database: Database
  _token_hasher: TokenHasher
  _ttl: timedelta

  def __init__(
    self,
    token_issuer_config: TokenIssuerConfig,
    database: Database,
    token_hasher: TokenHasher
  ):
    self._database = database
    self._token_hasher = token_hasher
    self._ttl = timedelta(days=token_issuer_config.time_to_live_days)

  def issue(self, *, user_ulid: str) -> str:
    plaintext_token = secrets.token_urlsafe(32)
    token_hash = self._token_hasher.hash(plaintext_token)
    expires_at = datetime.now(tz=timezone.utc) + self._ttl
    auth_token = AuthTokenORM(
      user_ulid=user_ulid,
      token_hash=token_hash,
      expires_at=expires_at,
      revoked_at=None,
    )
    with self._database.get_session() as session:
      session.add(auth_token)
      session.commit()
    return plaintext_token
