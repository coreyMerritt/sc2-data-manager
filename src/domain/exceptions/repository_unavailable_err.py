from domain.exceptions.domain_exception import DomainException


class RepositoryUnavailableErr(DomainException):
  message: str

  def __init__(self, *args):
    message="Repository is unavailable."
    self.message = message
    super().__init__(message, *args)
