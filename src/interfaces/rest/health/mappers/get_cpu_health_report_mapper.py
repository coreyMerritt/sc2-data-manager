from infrastructure.cpu.models.cpu_health_report import CpuHealthReport
from interfaces.rest.health.dto.res.get_cpu_health_report_res import GetCpuHealthReportRes


class GetCpuHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: CpuHealthReport) -> GetCpuHealthReportRes:
    return GetCpuHealthReportRes(
      usage_percentage=model.usage_percentage,
      healthy=model.healthy
    )
