from datetime import datetime
from typing import List, cast

from sc2reader.utils import Length
from sc2reader.objects import BuildEntry, Graph
from sc2reader.resources import GameSummary, PlayerSummary

from infrastructure.database.orm.account_orm import AccountORM
from infrastructure.database.orm.build_entry_orm import BuildEntryORM
from infrastructure.database.orm.build_order_orm import BuildOrderORM
from infrastructure.database.orm.game_participant_orm import GameParticipantORM
from infrastructure.database.orm.game_summary_orm import GameSummaryORM
from infrastructure.database.orm.graph_point_orm import GraphPointORM


class GraphPointsMapper:
  @staticmethod
  def domain_to_orm(game_summary: GameSummary) -> List[List[GraphPointORM]]:
    assert len(game_summary.players) == 2
    assert len(game_summary.player) == 2
    player_owned_graph_points: List[List[GraphPointORM]] = []
    for i in range(0, 2):
      player = game_summary.players[i]
      assert isinstance(player, PlayerSummary)
      player_stats = game_summary.player_stats[i]
      assert isinstance(player_stats, dict)
      graph_points: List[GraphPointORM] = []
      try:
        army_graph: Graph = cast(Graph, player.army_graph)
        if army_graph is not None:
          for x, y in army_graph.as_points():
            graph_points.append(GraphPointORM(
              graph_type="army",
              x=x,
              y=y
            ))
      except KeyError:
        pass
      try:
        income_graph: Graph = cast(Graph, player.income_graph)
        for x, y in income_graph.as_points():
          graph_points.append(GraphPointORM(
            graph_type="income",
            x=x,
            y=y
          ))
      except KeyError:
        pass
      try:
        resource_collection_rate_graph: Graph = cast(Graph, player_stats['Resource Collection Rate'])
        for x, y in resource_collection_rate_graph.as_points():
          graph_points.append(GraphPointORM(
            graph_type="resource_collection_rate",
            x=x,
            y=y
          ))
      except KeyError:
        pass
      try:
        upgrade_spending_graph: Graph = cast(Graph, player_stats['Upgrade Spending'])
        for x, y in upgrade_spending_graph.as_points():
          graph_points.append(GraphPointORM(
            graph_type="upgrade_spending",
            x=x,
            y=y
          ))
      except KeyError:
        pass
      try:
        workers_active_graph: Graph = cast(Graph, player_stats['Workers Active'])
        for x, y in workers_active_graph.as_points():
          graph_points.append(GraphPointORM(
            graph_type="workers_active",
            x=x,
            y=y
          ))
      except KeyError:
        pass
      player_owned_graph_points.append(graph_points)
    return player_owned_graph_points
