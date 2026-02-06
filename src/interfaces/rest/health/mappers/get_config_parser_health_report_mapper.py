from infrastructure.config.models.config_parser_health_report import ConfigParserHealthReport
from interfaces.rest.health.dto.res.get_config_parser_health_report_res import GetConfigParserHealthReportRes


class GetConfigParserHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: ConfigParserHealthReport) -> GetConfigParserHealthReportRes:
    return GetConfigParserHealthReportRes(
      healthy=model.healthy
    )
