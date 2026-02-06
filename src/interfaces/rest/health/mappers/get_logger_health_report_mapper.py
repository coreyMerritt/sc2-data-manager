from infrastructure.logger.models.logger_health_report import LoggerHealthReport
from interfaces.rest.health.dto.res.get_full_health_report_res import GetLoggerHealthReportRes


class GetLoggerHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: LoggerHealthReport) -> GetLoggerHealthReportRes:
    return GetLoggerHealthReportRes(
      healthy=model.healthy
    )
