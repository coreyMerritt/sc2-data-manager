import psutil

from infrastructure.base_infrastructure import BaseInfrastructure
from infrastructure.cpu.models.cpu_config import CpuConfig
from infrastructure.cpu.models.cpu_health_report import CpuHealthReport


class Cpu(BaseInfrastructure):
  _check_interval_seconds: float
  _maximum_healthy_usage_percentage: float

  def __init__(self, cpu_config: CpuConfig):
    self._check_interval_seconds = cpu_config.check_interval_seconds
    self._maximum_healthy_usage_percentage = cpu_config.maximum_healthy_usage_percentage
    super().__init__()

  def get_health_report(self) -> CpuHealthReport:
    maximum_healthy_usage_percentage = self._maximum_healthy_usage_percentage
    usage_percentage = self.get_cpu_usage_percentage()
    healthy = usage_percentage <= maximum_healthy_usage_percentage
    return CpuHealthReport(
      usage_percentage=usage_percentage,
      healthy=healthy
    )

  def get_cpu_usage_percentage(self) -> float:
    return psutil.cpu_percent(
      interval=self._check_interval_seconds
    )
