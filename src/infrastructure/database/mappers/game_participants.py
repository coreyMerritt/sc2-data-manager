import pprint
from typing import List

from sc2reader.resources import GameSummary, PlayerSummary

from infrastructure.database.orm.game_participant_orm import GameParticipantORM


class GameParticipantsMapper:
  @staticmethod
  def domain_to_orm(game_summary: GameSummary) -> List[GameParticipantORM]:
    assert len(game_summary.players) == 2
    assert len(game_summary.player) == 2
    participant_orms: List[GameParticipantORM] = []
    for i in range(0, 2):
      player = game_summary.players[i]
      assert isinstance(player, PlayerSummary)
      player_stats = game_summary.player_stats[i]
      assert isinstance(player_stats, dict)
      player_settings = game_summary.player_settings[i]
      assert isinstance(player_settings, dict)
      if 'Technology' in player_stats:
        technology = player_stats['Technology']
      else:
        technology = 0
      if 'Structures Built' in player_stats:
        structures_built = player_stats['Structures Built']
      else:
        structures_built = 0
      if 'Killed Unit Count' in player_stats:
        killed_unit_count = player_stats['Killed Unit Count']
      else:
        killed_unit_count = 0
      participant_orm = GameParticipantORM(
        game_filehash=game_summary.filehash,
        account_bnetid=player.bnetid,
        is_ai=player.is_ai,
        is_winner=player.is_winner,
        apm=player_stats['APM'],
        average_unspent_resources=player_stats['Average Unspent Resources'],
        overview=player_stats['Overview'],
        resources_destroyed=player_stats['Enemies Destroyed:'],
        resources_mined=player_stats['Resources'],
        resources_spent=player_stats['Resources Spent:'],
        resources_spent_on_structures=player_stats['Structures'],
        resources_spent_on_technology=technology,
        resources_spent_on_units=player_stats['Units'],
        structures_built=structures_built,
        structures_killed=player_stats['Structures Razed Count'],
        subregion=player.subregion,
        time_supply_capped=player_stats['Time Supply Capped'],
        units_killed=killed_unit_count,
        units_trained=player_stats['Units Trained'],
        workers_created=player_stats['Workers Created'],
        color=player_settings['Color'],
        pick_race=player.pick_race,
        play_race=player.play_race or player.pick_race,
        region=player.region
      )
      participant_orms.append(participant_orm)
    return participant_orms
