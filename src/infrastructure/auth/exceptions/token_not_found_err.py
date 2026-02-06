from infrastructure.exceptions.infrastructure_exception import BaseInfrastructureException


class TokenNotFoundErr(BaseInfrastructureException):
  message: str

  def __init__(self, *args):
    message="Auth token not found."
    self.message = message
    super().__init__(message, *args)
