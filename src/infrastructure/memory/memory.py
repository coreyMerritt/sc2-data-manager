import psutil

from infrastructure.base_infrastructure import BaseInfrastructure
from infrastructure.memory.models.memory_config import MemoryConfig
from infrastructure.memory.models.memory_health_report import MemoryHealthReport


class Memory(BaseInfrastructure):
  _maximum_healthy_usage_percentage: float

  def __init__(self, memory_config: MemoryConfig):
    self._maximum_healthy_usage_percentage = memory_config.maximum_healthy_usage_percentage
    super().__init__()

  def get_health_report(self) -> MemoryHealthReport:
    maximum_healthy_usage_percentage = self._maximum_healthy_usage_percentage
    usage_percentage = self.get_memory_usage_percentage()
    healthy = usage_percentage <= maximum_healthy_usage_percentage
    return MemoryHealthReport(
      usage_percentage=usage_percentage,
      healthy=healthy
    )

  def get_memory_usage_percentage(self) -> float:
    return psutil.virtual_memory().percent
