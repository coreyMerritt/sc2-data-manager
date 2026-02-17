from typing import TYPE_CHECKING, ClassVar
from sqlmodel import Field, ForeignKeyConstraint, Relationship, SQLModel


if TYPE_CHECKING:
  from infrastructure.database.orm.account_orm import AccountORM
  from infrastructure.database.orm.build_order_orm import BuildOrderORM
  from infrastructure.database.orm.game_summary_orm import GameSummaryORM
  from infrastructure.database.orm.graph_point_orm import GraphPointORM


class GameParticipantORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "game_participant"
  __table_args__ = (
    ForeignKeyConstraint(
        ["account_bnetid", "account_region"],
        ["account.bnetid", "account.region"],
    ),
  )
  account_bnetid: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  account_region: str = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )

  id: int | None = Field(
    primary_key=True,
    unique=True,
    nullable=False,
    default=None
  )

  game_filehash: str = Field(
    primary_key=False,
    unique=False,
    nullable=False,
    foreign_key="game_summary.filehash"
  )

  is_ai: bool = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  is_winner: bool = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  apm: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  average_unspent_resources: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  overview: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  resources_destroyed: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  resources_mined: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  resources_spent: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  resources_spent_on_structures: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  resources_spent_on_technology: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  resources_spent_on_units: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  structures_built: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  structures_killed: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  subregion: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  time_supply_capped: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  units_killed: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  units_trained: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  workers_created: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  color: str = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  pick_race: str = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  play_race: str = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  region: str = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )

  account: "AccountORM" = Relationship(back_populates="game_participants")
  build_order: "BuildOrderORM" = Relationship(back_populates="game_participant")
  game_summary: "GameSummaryORM" = Relationship(back_populates="game_participants")
  graph_points: list["GraphPointORM"] = Relationship(back_populates="game_participant")

  @property
  def army_graph_points(self):
    return [g for g in self.graph_points if g.graph_type == "army"]
  @property
  def income_graph_points(self):
    return [g for g in self.graph_points if g.graph_type == "income"]
  @property
  def resource_collection_rate_graph_points(self):    # TODO: This might be the same as income -- need to double check
    return [g for g in self.graph_points if g.graph_type == "resource_collection_rate"]
  @property
  def upgrade_spending_graph_points(self):     # x.player_stats[x]['Upgrade Spending'].to_points()
    return [g for g in self.graph_points if g.graph_type == "upgrade_spending"]
  @property
  def workers_active_graph_points(self):     # x.player_stats[x]['Workers Active'].to_points()
    return [g for g in self.graph_points if g.graph_type == "workers_active"]
