import asyncio

from fastapi import Request

from interfaces.rest.models.sc2_data_manager_http_response import SC2DataManagerHTTPResponse
from services.exceptions.item_creation_err import ItemCreationErr


class GameSummaryController:
  async def create_game_summary(self, req: Request) -> SC2DataManagerHTTPResponse:
    game_summary_manager = GameSummaryManager(
      user_admin_secret=req.app.state.resources.vars.users_admin_secret,
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user
    )
    create_game_summary_service_model = CreateGameSummaryMapper.req_to_sim(body)
    create_game_summary_som = await asyncio.to_thread(game_summary_manager.create_game_summary, create_game_summary_service_model)
    if not create_game_summary_som:
      raise ItemCreationErr()
    create_game_summary_res = CreateGameSummaryMapper.som_to_res(create_game_summary_som)
    return SC2DataManagerHTTPResponse(
      data=create_game_summary_res
    )
