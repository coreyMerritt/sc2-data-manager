import asyncio

from fastapi import Request

from interfaces.rest.models.sc2_data_manager_http_response import SC2DataManagerHTTPResponse
from interfaces.rest.v1.mappers.game_summary.create_game_summary_mapper import CreateGameSummaryMapper
from services.game_summary_manager import GameSummaryManager


class GameSummaryController:
  async def create_game_summary(self, req: Request) -> SC2DataManagerHTTPResponse:
    game_summary_manager = GameSummaryManager(
      disk=req.app.state.resources.infra.disk,
      logger=req.app.state.resources.infra.logger,
      account_repository=req.app.state.resources.repos.account,
      game_summary_repository=req.app.state.resources.repos.game_summary
    )
    create_user_som = await asyncio.to_thread(game_summary_manager.ingest_game_summary, await req.body())
    create_game_summary_res = CreateGameSummaryMapper.som_to_res(create_user_som)
    return SC2DataManagerHTTPResponse(
      data=create_game_summary_res
    )
