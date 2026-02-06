from dataclasses import dataclass

from infrastructure.logger.models.logs.base_log import BaseLog
from infrastructure.logger.models.logs.ids import IDs
from infrastructure.logger.models.logs.status import Status


@dataclass
class HTTPResponseLog(BaseLog):
  ids: IDs
  status: Status
  duration_ms: float
