from datetime import datetime

from sc2reader.utils import Length
from sc2reader.resources import GameSummary

from infrastructure.database.orm.game_summary_orm import GameSummaryORM


class GameSummaryMapper:
  @staticmethod
  def domain_to_orm(game_summary: GameSummary) -> GameSummaryORM:
    assert game_summary.game_speed == game_summary.settings['Game Speed']
    if isinstance(game_summary.game_length, int):
      game_length = game_summary.game_length
    elif isinstance(game_summary.game_length, Length):
      game_length = game_summary.game_length.seconds
    if isinstance(game_summary.real_length, int):
      real_length = game_summary.real_length
    elif isinstance(game_summary.real_length, Length):
      real_length = game_summary.real_length.seconds
    if game_summary.real_type:
      game_type = game_summary.real_type
    else:
      game_type = game_summary.game_type
    assert game_type is not None
    assert isinstance(game_summary.start_time, datetime)
    assert isinstance(game_summary.end_time, datetime)
    game_summary_orm = GameSummaryORM(
      is_ladder=game_summary.settings['Game Mode'] == 'Automated Match Making',
      game_length_blizzard_seconds=game_length,
      game_length_real_seconds=real_length,
      filehash=game_summary.filehash,
      filename=game_summary.filename,
      game_speed=game_summary.game_speed,
      game_type=game_summary.game_type,
      map_name=game_summary.map_name,
      end_time=game_summary.end_time,
      start_time=game_summary.start_time
    )
    return game_summary_orm
