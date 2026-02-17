from interfaces.rest.v1.dto.res.game_summary.create_game_summary_res import CreateGameSummaryRes
from services.models.outputs.game_summary.create_game_summary_som import CreateGameSummarySOM


class CreateGameSummaryMapper:
  @staticmethod
  def som_to_res(som: CreateGameSummarySOM) -> CreateGameSummaryRes:
    return CreateGameSummaryRes(
      filehash=som.filehash
    )
