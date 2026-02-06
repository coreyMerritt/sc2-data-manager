from shared.enums.exception_type import ExceptionType
from shared.exceptions.sc2_data_manager_exception import SC2DataManagerException


class DomainException(SC2DataManagerException):
  exception_type = ExceptionType.DOMAIN
