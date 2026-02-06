from interfaces.rest.health.dto.res.get_full_health_report_res import GetFullHealthReportRes
from interfaces.rest.health.mappers.get_config_parser_health_report_mapper import GetConfigParserHealthReportMapper
from interfaces.rest.health.mappers.get_cpu_health_report_mapper import GetCpuHealthReportMapper
from interfaces.rest.health.mappers.get_database_health_report_mapper import GetDatabaseHealthReportMapper
from interfaces.rest.health.mappers.get_disk_health_report_mapper import GetDiskHealthReportMapper
from interfaces.rest.health.mappers.get_environment_health_report_mapper import GetEnvironmentHealthReportMapper
from interfaces.rest.health.mappers.get_logger_health_report_mapper import GetLoggerHealthReportMapper
from interfaces.rest.health.mappers.get_memory_health_report_mapper import GetMemoryHealthReportMapper
from services.models.outputs.full_health_report_som import FullHealthReportSOM


class GetFullHealthReportMapper:
  @staticmethod
  def som_to_res(som: FullHealthReportSOM) -> GetFullHealthReportRes:
    get_config_parser_health_report_res = GetConfigParserHealthReportMapper.infrastructure_model_to_res(
      som.config_parser_health_report
    )
    get_cpu_health_report_res = GetCpuHealthReportMapper.infrastructure_model_to_res(
      som.cpu_health_report
    )
    get_database_health_report_res = GetDatabaseHealthReportMapper.infrastructure_model_to_res(
      som.database_health_report
    )
    get_disk_health_report_res = GetDiskHealthReportMapper.infrastructure_model_to_res(
      som.disk_health_report
    )
    get_environment_health_report_res = GetEnvironmentHealthReportMapper.infrastructure_model_to_res(
      som.environment_health_report
    )
    get_logger_health_report_res = GetLoggerHealthReportMapper.infrastructure_model_to_res(
      som.logger_health_report
    )
    get_memory_health_report_res = GetMemoryHealthReportMapper.infrastructure_model_to_res(
      som.memory_health_report
    )
    return GetFullHealthReportRes(
      config_parser=get_config_parser_health_report_res,
      cpu=get_cpu_health_report_res,
      database=get_database_health_report_res,
      disk=get_disk_health_report_res,
      environment=get_environment_health_report_res,
      logger=get_logger_health_report_res,
      memory=get_memory_health_report_res,
      healthy=som.healthy
    )
