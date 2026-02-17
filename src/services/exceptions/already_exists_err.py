from services.exceptions.base_service_exception import BaseServiceException


class AlreadyExistsErr(BaseServiceException):
  message: str

  def __init__(self, *args):
    message="Item already exists."
    self.message = message
    super().__init__(message, *args)
