from fastapi import APIRouter, Request

from interfaces.rest.health.controllers.health_controller import HealthController
from interfaces.rest.models.sc2_data_manager_http_response import SC2DataManagerHTTPResponse

controller = HealthController()
router = APIRouter(prefix="/api/health")

@router.get("", response_model=SC2DataManagerHTTPResponse)
async def get_simple_health_report(req: Request) -> SC2DataManagerHTTPResponse:
  return await controller.get_simple_health_report(
    req=req
  )

@router.get("/full", response_model=SC2DataManagerHTTPResponse)
async def get_full_health_report(req: Request) -> SC2DataManagerHTTPResponse:
  return await controller.get_full_health_report(
    req=req
  )
