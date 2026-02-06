from services.exceptions.base_service_exception import BaseServiceException


class ServiceUnavailableErr(BaseServiceException):
  message: str

  def __init__(self, *args):
    message="Service unavailable."
    self.message = message
    super().__init__(message, *args)
