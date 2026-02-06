from infrastructure.memory.models.memory_health_report import MemoryHealthReport
from interfaces.rest.health.dto.res.get_memory_health_report_res import GetMemoryHealthReportRes


class GetMemoryHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: MemoryHealthReport) -> GetMemoryHealthReportRes:
    return GetMemoryHealthReportRes(
      usage_percentage=model.usage_percentage,
      healthy=model.healthy
    )
