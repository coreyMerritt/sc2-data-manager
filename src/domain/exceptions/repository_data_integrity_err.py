from domain.exceptions.domain_exception import DomainException


class RepositoryDataIntegrityErr(DomainException):
  message: str

  def __init__(self, *args):
    message="Data integrity seems to be compromised."
    self.message = message
    super().__init__(message, *args)
