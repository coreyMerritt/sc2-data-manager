from typing import List

from sc2reader.objects import BuildEntry
from sc2reader.resources import GameSummary

from infrastructure.database.orm.build_entry_orm import BuildEntryORM
from infrastructure.database.orm.build_order_orm import BuildOrderORM


class BuildOrdersMapper:
  @staticmethod
  def domain_to_orm(game_summary: GameSummary) -> List[BuildOrderORM]:
    assert len(game_summary.players) == 2
    assert len(game_summary.player) == 2
    build_order_orms: List[BuildOrderORM] = []
    for i in range(0, 2):
      build_entries: List[BuildEntryORM] = []
      for entry in game_summary.build_orders[i]:
        assert isinstance(entry, BuildEntry)
        build_entries.append(BuildEntryORM(
          item_name=entry.order,
          supply=entry.supply,
          supply_total=entry.total_supply,
          timestamp=entry.time,
        ))
      build_order_orm = BuildOrderORM(
        build_entries=build_entries
      )
      build_order_orms.append(build_order_orm)
    return build_order_orms
