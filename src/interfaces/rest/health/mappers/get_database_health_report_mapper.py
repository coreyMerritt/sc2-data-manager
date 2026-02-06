from infrastructure.database.models.database_health_report import DatabaseHealthReport
from interfaces.rest.health.dto.res.get_full_health_report_res import GetDatabaseHealthReportRes


class GetDatabaseHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: DatabaseHealthReport) -> GetDatabaseHealthReportRes:
    return GetDatabaseHealthReportRes(
      healthy=model.healthy
    )
