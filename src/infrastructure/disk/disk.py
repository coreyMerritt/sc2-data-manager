from typing import Any

import psutil
import yaml

from infrastructure.base_infrastructure import BaseInfrastructure
from infrastructure.disk.exceptions.disk_read_err import DiskReadErr
from infrastructure.disk.models.disk_config import DiskConfig
from infrastructure.disk.models.disk_health_report import DiskHealthReport


class Disk(BaseInfrastructure):
  _maximum_healthy_usage_percentage: float

  def __init__(self, disk_config: DiskConfig):
    self._maximum_healthy_usage_percentage = disk_config.maximum_healthy_usage_percentage
    super().__init__()

  def get_health_report(self) -> DiskHealthReport:
    maximum_healthy_usage_percentage = self._maximum_healthy_usage_percentage
    usage_percentage = self._get_disk_usage_percentage()
    healthy = usage_percentage <= maximum_healthy_usage_percentage
    return DiskHealthReport(
      usage_percentage=usage_percentage,
      healthy=healthy
    )

  def read_yaml(self, yaml_path: str) -> Any:
    try:
      with open(yaml_path, "r", encoding='utf-8') as yaml_file:
        some_data = yaml.safe_load(yaml_file)
        return some_data
    except Exception as e:
      raise DiskReadErr(
        filename=yaml_path
      ) from e

  def _get_disk_usage_percentage(self) -> float:
    return psutil.disk_usage("/").percent
