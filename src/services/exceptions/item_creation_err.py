from services.exceptions.base_service_exception import BaseServiceException


class ItemCreationErr(BaseServiceException):
  message: str

  def __init__(self, *args):
    message="Failed to create item."
    self.message = message
    super().__init__(message, *args)
