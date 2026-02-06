from infrastructure.exceptions.infrastructure_exception import BaseInfrastructureException


class TokenRevokedErr(BaseInfrastructureException):
  message: str

  def __init__(self, *args):
    message="Auth token revoked."
    self.message = message
    super().__init__(message, *args)
