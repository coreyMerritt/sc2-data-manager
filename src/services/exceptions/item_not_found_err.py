from services.exceptions.base_service_exception import BaseServiceException


class ItemNotFoundErr(BaseServiceException):
  message: str

  def __init__(self, *args):
    message="Failed to retrieve item."
    self.message = message
    super().__init__(message, *args)
