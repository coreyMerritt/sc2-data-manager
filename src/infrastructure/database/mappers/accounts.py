from typing import List

from sc2reader.resources import GameSummary, PlayerSummary

from infrastructure.database.orm.account_orm import AccountORM


class AccountsMapper:
  @staticmethod
  def domain_to_orm(game_summary: GameSummary) -> List[AccountORM]:
    assert len(game_summary.players) == 2
    assert len(game_summary.player) == 2
    account_orms: List[AccountORM] = []
    for i in range(0, 2):
      player = game_summary.players[i]
      assert isinstance(player, PlayerSummary)
      account_orm = AccountORM(
        name=None,
        bnetid=player.bnetid,
        region=player.region
      )
      account_orms.append(account_orm)
    return account_orms