from services.exceptions.base_service_exception import BaseServiceException


class ServiceInitializationErr(BaseServiceException):
  message: str

  def __init__(self, *args):
    message="Failed to initialize service."
    self.message = message
    super().__init__(message, *args)
