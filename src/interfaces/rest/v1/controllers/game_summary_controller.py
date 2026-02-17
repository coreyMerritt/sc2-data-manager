import asyncio

from fastapi import Request

from interfaces.rest.models.sc2_data_manager_http_response import SC2DataManagerHTTPResponse
from services.game_summary_manager import GameSummaryManager


class GameSummaryController:
  async def create_game_summary(self, req: Request) -> SC2DataManagerHTTPResponse:
    game_summary_manager = GameSummaryManager(
      user_admin_secret=req.app.state.resources.vars.users_admin_secret,
      disk=req.app.state.resources.infra.disk,
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user
    )
    await asyncio.to_thread(game_summary_manager.ingest_game_summary, req.body())
    return SC2DataManagerHTTPResponse(
      data="Success"
    )
