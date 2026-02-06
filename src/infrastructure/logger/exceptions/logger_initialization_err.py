from infrastructure.exceptions.infrastructure_exception import BaseInfrastructureException


class LoggerInitializationErr(BaseInfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to initialize logger."
    self.message = message
    super().__init__(message, *args)
