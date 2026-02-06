from infrastructure.exceptions.infrastructure_exception import BaseInfrastructureException


class TokenExpiredErr(BaseInfrastructureException):
  message: str

  def __init__(self, *args):
    message="Auth token expired."
    self.message = message
    super().__init__(message, *args)
