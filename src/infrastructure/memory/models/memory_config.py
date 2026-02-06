from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryConfig():
  maximum_healthy_usage_percentage: float
