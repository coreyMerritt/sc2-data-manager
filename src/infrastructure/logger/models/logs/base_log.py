from dataclasses import dataclass

from infrastructure.logger.models.logs.error import Error
from infrastructure.logger.models.logs.timestamps import Timestamps


@dataclass
class BaseLog:
  message: str
  level: str
  timestamps: Timestamps
  error: Error | None

  def __post_init__(self):
    assert type(self) is not BaseLog, "BaseLog is a base class and should not be instantiated"
