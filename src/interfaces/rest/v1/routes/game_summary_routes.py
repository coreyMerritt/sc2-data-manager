from fastapi import APIRouter, Request

from interfaces.rest.models.sc2_data_manager_http_response import SC2DataManagerHTTPResponse
from interfaces.rest.v1.controllers.game_summary_controller import GameSummaryController

controller = GameSummaryController()
router = APIRouter(prefix="/api/v1/game_summaries")

@router.post(
  path="",
  response_model=SC2DataManagerHTTPResponse,
  status_code=201
)
async def create_game_summary(
  req: Request
) -> SC2DataManagerHTTPResponse:
  return await controller.create_user(
    req=req
  )
