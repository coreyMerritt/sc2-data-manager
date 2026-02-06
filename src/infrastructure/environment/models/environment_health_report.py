from dataclasses import dataclass

from infrastructure.models.base_health_report import HealthReport


@dataclass
class EnvironmentHealthReport(HealthReport):
  """ Only contains base health report values """
