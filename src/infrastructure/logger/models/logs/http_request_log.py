from dataclasses import dataclass

from infrastructure.logger.models.logs.base_log import BaseLog
from infrastructure.logger.models.logs.ids import IDs


@dataclass
class HTTPRequestLog(BaseLog):
  ids: IDs
  client_ip: str
  endpoint: str
  method: str
  route: str
  user_agent: str
