from interfaces.rest.health.dto.res.base_get_health_report_res import GetHealthReportRes
from interfaces.rest.health.dto.res.get_config_parser_health_report_res import GetConfigParserHealthReportRes
from interfaces.rest.health.dto.res.get_cpu_health_report_res import GetCpuHealthReportRes
from interfaces.rest.health.dto.res.get_database_health_report_res import GetDatabaseHealthReportRes
from interfaces.rest.health.dto.res.get_disk_health_report_res import GetDiskHealthReportRes
from interfaces.rest.health.dto.res.get_environment_health_report_res import GetEnvironmentHealthReportRes
from interfaces.rest.health.dto.res.get_logger_health_report_res import GetLoggerHealthReportRes
from interfaces.rest.health.dto.res.get_memory_health_report_res import GetMemoryHealthReportRes


class GetFullHealthReportRes(GetHealthReportRes):
  config_parser: GetConfigParserHealthReportRes
  cpu: GetCpuHealthReportRes
  database: GetDatabaseHealthReportRes
  disk: GetDiskHealthReportRes
  environment: GetEnvironmentHealthReportRes
  logger: GetLoggerHealthReportRes
  memory: GetMemoryHealthReportRes
