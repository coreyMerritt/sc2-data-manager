from infrastructure.exceptions.infrastructure_exception import BaseInfrastructureException


class DatabaseInitializationErr(BaseInfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to initialize database."
    self.message = message
    super().__init__(message, *args)
