from domain.exceptions.domain_exception import DomainException


class RepositoryDuplicationErr(DomainException):
  message: str

  def __init__(self, *args):
    message="Attempted to create duplicate data where it is not allowed."
    self.message = message
    super().__init__(message, *args)
