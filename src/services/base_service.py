from domain.exceptions.repository_data_integrity_err import RepositoryDataIntegrityErr
from domain.exceptions.repository_duplication_err import RepositoryDuplicationErr
from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from domain.exceptions.validation_err import ValidationErr
from infrastructure.types.logger_interface import LoggerInterface
from services.exceptions.bad_input_err import BadInputErr
from services.exceptions.base_service_exception import BaseServiceException
from services.exceptions.item_not_found_err import ItemNotFoundErr
from services.exceptions.service_unavailable_err import ServiceUnavailableErr
from services.exceptions.uniqueness_violation_err import UniquenessViolationErr


class BaseService():
  _logger: LoggerInterface

  def __init__(self, logger: LoggerInterface):
    self._logger = logger
    assert type(self) is not BaseService, "BaseService is a base class and should not be instantiated"

  def _raise_service_exception(self, e: Exception) -> None:
    # Children of BaseServiceException will be passed directly to interfaces
    if isinstance(e, BaseServiceException):
      raise e
    # Exception translation for domain/infra -- explicit catches will stop this from triggering
    mapping = {
      RepositoryDataIntegrityErr: BadInputErr,
      RepositoryDuplicationErr: UniquenessViolationErr,
      RepositoryNotFoundErr: ItemNotFoundErr,
      RepositoryUnavailableErr: ServiceUnavailableErr,
      ValidationErr: BadInputErr,
    }
    for error_type, service_error in mapping.items():
      if isinstance(e, error_type):
        raise service_error() from e
    raise ServiceUnavailableErr() from e
