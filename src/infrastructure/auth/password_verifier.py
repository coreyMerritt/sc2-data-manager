import bcrypt


class PasswordVerifier:
  def verify(self, *, plaintext: str, hashed: str) -> bool:
    if not plaintext or not hashed:
      return False
    try:
      return bcrypt.checkpw(
        plaintext.encode("utf-8"),
        hashed.encode("utf-8"),
      )
    except ValueError:
      return False
