from services.exceptions.base_service_exception import BaseServiceException


class BadInputErr(BaseServiceException):
  message: str

  def __init__(self, *args):
    message="Bad input."
    self.message = message
    super().__init__(message, *args)
