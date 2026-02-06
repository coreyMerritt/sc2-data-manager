import asyncio

from fastapi import HTTPException, Request

from domain.enums.user_type import UserType
from domain.subdomain.entities.user import User
from interfaces.rest.health.mappers.get_full_health_report_mapper import GetFullHealthReportMapper
from interfaces.rest.health.mappers.get_simple_health_report_mapper import GetSimpleHealthReportMapper
from interfaces.rest.models.sc2_data_manager_http_response import SC2DataManagerHTTPResponse
from services.health_manager import HealthManager
from services.models.outputs.full_health_report_som import FullHealthReportSOM


class HealthController:
  async def get_simple_health_report(self, req: Request) -> SC2DataManagerHTTPResponse:
    health_report_som = await self._get_health_report_som(req)
    get_simple_health_report_res = GetSimpleHealthReportMapper.som_to_res(health_report_som)
    return SC2DataManagerHTTPResponse(
      data=get_simple_health_report_res
    )

  async def get_full_health_report(self, req: Request) -> SC2DataManagerHTTPResponse:
    authenticated_user: User = req.state.user
    if (
      not getattr(req.state, "is_authenticated", False)
      or not getattr(req.state, "user", None)
      or authenticated_user.user_type not in (
        UserType.ADMIN,
        UserType.WRITE_CLIENT,
        UserType.READ_ONLY_CLIENT
      )
    ):
      raise HTTPException(
        status_code=401,
        detail="Permission denied",
      )
    health_report_som = await self._get_health_report_som(req)
    get_full_health_report_res = GetFullHealthReportMapper.som_to_res(health_report_som)
    return SC2DataManagerHTTPResponse(
      data=get_full_health_report_res
    )

  async def _get_health_report_som(self, req: Request) -> FullHealthReportSOM:
    health_manager = HealthManager(
      logger=req.app.state.resources.infra.logger,
      config_parser=req.app.state.resources.infra.config_parser,
      cpu=req.app.state.resources.infra.cpu,
      database=req.app.state.resources.infra.database,
      disk=req.app.state.resources.infra.disk,
      environment=req.app.state.resources.infra.environment,
      memory=req.app.state.resources.infra.memory
    )
    return await asyncio.to_thread(
      health_manager.get_full_health_report
    )
