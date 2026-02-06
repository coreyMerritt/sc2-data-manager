from infrastructure.environment.models.environment_health_report import EnvironmentHealthReport
from interfaces.rest.health.dto.res.get_environment_health_report_res import GetEnvironmentHealthReportRes


class GetEnvironmentHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: EnvironmentHealthReport) -> GetEnvironmentHealthReportRes:
    return GetEnvironmentHealthReportRes(
      healthy=model.healthy
    )
