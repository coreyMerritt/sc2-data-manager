from interfaces.rest.health.dto.res.get_simple_health_report_res import GetSimpleHealthReportRes
from services.models.outputs.full_health_report_som import FullHealthReportSOM


class GetSimpleHealthReportMapper:
  @staticmethod
  def som_to_res(som: FullHealthReportSOM) -> GetSimpleHealthReportRes:
    return GetSimpleHealthReportRes(
      healthy=som.healthy
    )
