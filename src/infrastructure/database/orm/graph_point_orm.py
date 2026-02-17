from typing import TYPE_CHECKING, ClassVar
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from infrastructure.database.orm.game_participant_orm import GameParticipantORM

class GraphPointORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "graph_point"
  id: int | None = Field(
    primary_key=True,
    unique=True,
    nullable=False,
    default=None
  )
  game_participant_id: int | None = Field(
    primary_key=False,
    unique=False,
    nullable=False,
    default=None,
    foreign_key="game_participant.id"
  )

  graph_type: str = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  x: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  y: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )

  game_participant: "GameParticipantORM" = Relationship(back_populates="graph_points")
