from interfaces.rest.health.dto.res.base_get_health_report_res import GetHealthReportRes


class GetMemoryHealthReportRes(GetHealthReportRes):
  usage_percentage: float
