from dataclasses import dataclass


@dataclass(frozen=True)
class DiskConfig():
  maximum_healthy_usage_percentage: float
