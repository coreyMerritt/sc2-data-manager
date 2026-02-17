from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
  from infrastructure.database.orm.game_participant_orm import GameParticipantORM


class GameSummaryORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "game_summary"
  filehash: str = Field(
    primary_key=True,
    unique=True,
    nullable=False
  )

  is_ladder: bool = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  game_length_real_seconds: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  game_length_blizzard_seconds: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  filename: str = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  game_speed: str = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  game_type: str = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  map_name: str = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  end_time: datetime = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  start_time: datetime = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )

  game_participants: List["GameParticipantORM"] = Relationship(back_populates="game_summary")
