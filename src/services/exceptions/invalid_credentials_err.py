from services.exceptions.base_service_exception import BaseServiceException


class InvalidCredentialsErr(BaseServiceException):
  message: str

  def __init__(self, *args):
    message="Invalid credentials."
    self.message = message
    super().__init__(message, *args)
