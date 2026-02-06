from dataclasses import dataclass

from infrastructure.models.base_health_report import HealthReport


@dataclass
class DiskHealthReport(HealthReport):
  usage_percentage: float
