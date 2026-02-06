from dataclasses import dataclass

from infrastructure.models.base_health_report import HealthReport


@dataclass
class CpuHealthReport(HealthReport):
  usage_percentage: float
