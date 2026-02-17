from io import BytesIO

from sc2reader.factories import SC2Factory
from sc2reader.resources import GameSummary


class CreateGameSummaryMapper:
  @staticmethod
  def byte_string_to_entity(byte_string: bytes) -> GameSummary:
    game_summary: GameSummary = SC2Factory().load_game_summary(BytesIO(byte_string))
    return game_summary
