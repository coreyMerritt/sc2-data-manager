import bcrypt


class PasswordHasher:
  def hash(self, plaintext: str) -> str:
    if not plaintext:
      raise ValueError("Password must not be empty")
    hashed = bcrypt.hashpw(
      plaintext.encode("utf-8"),
      bcrypt.gensalt(),
    )
    return hashed.decode("utf-8")
