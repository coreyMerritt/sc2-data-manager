from interfaces.rest.health.dto.res.base_get_health_report_res import GetHealthReportRes


class GetCpuHealthReportRes(GetHealthReportRes):
  usage_percentage: float
