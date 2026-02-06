from dataclasses import dataclass


@dataclass(frozen=True)
class CpuConfig():
  check_interval_seconds: float
  maximum_healthy_usage_percentage: float
