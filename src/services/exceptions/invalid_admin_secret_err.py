from services.exceptions.base_service_exception import BaseServiceException


class InvalidAdminSecretErr(BaseServiceException):
  message: str

  def __init__(self, *args):
    message="Invalid admin secret."
    self.message = message
    super().__init__(message, *args)
