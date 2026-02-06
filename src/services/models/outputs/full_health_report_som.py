from dataclasses import dataclass, field

from infrastructure.config.models.config_parser_health_report import ConfigParserHealthReport
from infrastructure.cpu.models.cpu_health_report import CpuHealthReport
from infrastructure.database.models.database_health_report import DatabaseHealthReport
from infrastructure.disk.models.disk_health_report import DiskHealthReport
from infrastructure.environment.models.environment_health_report import EnvironmentHealthReport
from infrastructure.logger.models.logger_health_report import LoggerHealthReport
from infrastructure.memory.models.memory_health_report import MemoryHealthReport


@dataclass
class FullHealthReportSOM():
  healthy: bool = field(init=False)
  config_parser_health_report: ConfigParserHealthReport
  cpu_health_report: CpuHealthReport
  database_health_report: DatabaseHealthReport
  disk_health_report: DiskHealthReport
  environment_health_report: EnvironmentHealthReport
  logger_health_report: LoggerHealthReport
  memory_health_report: MemoryHealthReport

  def __post_init__(self):
    self.healthy = (
      self.config_parser_health_report.healthy
      and self.cpu_health_report.healthy
      and self.database_health_report.healthy
      and self.disk_health_report.healthy
      and self.environment_health_report.healthy
      and self.logger_health_report.healthy
      and self.memory_health_report.healthy
    )
