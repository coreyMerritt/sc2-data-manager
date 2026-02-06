from domain.exceptions.domain_exception import DomainException


class RepositoryNotFoundErr(DomainException):
  message: str

  def __init__(self, *args):
    message="Item not found within Repository."
    self.message = message
    super().__init__(message, *args)
