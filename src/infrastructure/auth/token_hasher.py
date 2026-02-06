import hashlib
import hmac

from infrastructure.auth.models.token_hasher_config import TokenHasherConfig


class TokenHasher:
  def __init__(self, token_hasher_config: TokenHasherConfig):
    if not token_hasher_config.secret:
      raise ValueError("Token secret must not be empty")
    self._secret = token_hasher_config.secret

  def hash(self, token: str) -> str:
    if not token:
      raise ValueError("Token must not be empty")
    return hmac.new(
      key=self._secret.encode("utf-8"),
      msg=token.encode("utf-8"),
      digestmod=hashlib.sha256,
    ).hexdigest()
