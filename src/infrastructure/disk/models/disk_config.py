from dataclasses import dataclass


@dataclass(frozen=True)
class DiskConfig():
  game_summary_files_directory: str
  maximum_healthy_usage_percentage: float
