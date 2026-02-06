from domain.exceptions.domain_exception import DomainException


class ValidationErr(DomainException):
  attribute_name: str
  message: str

  def __init__(self, attribute_name: str, *args):
    message=f"Domain mapping error occurred on attribute: {attribute_name}"
    self.attribute_name = attribute_name
    self.message = message
    super().__init__(message, *args)
