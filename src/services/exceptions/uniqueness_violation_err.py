from services.exceptions.base_service_exception import BaseServiceException


class UniquenessViolationErr(BaseServiceException):
  message: str

  def __init__(self, *args):
    message="Attempted to create duplicate data where not permitted."
    self.message = message
    super().__init__(message, *args)
