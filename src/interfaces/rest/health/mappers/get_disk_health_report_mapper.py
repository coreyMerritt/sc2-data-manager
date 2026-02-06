from infrastructure.disk.models.disk_health_report import DiskHealthReport
from interfaces.rest.health.dto.res.get_disk_health_report_res import GetDiskHealthReportRes


class GetDiskHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: DiskHealthReport) -> GetDiskHealthReportRes:
    return GetDiskHealthReportRes(
      usage_percentage=model.usage_percentage,
      healthy=model.healthy
    )
