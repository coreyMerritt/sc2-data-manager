from abc import ABC, abstractmethod


class AuthenticatorInterface(ABC):
  @abstractmethod
  def authenticate(self, token: str) -> str:
    """
    Returns user_id if valid.
    Raises AuthFailedErr otherwise.
    """
    raise NotImplementedError
