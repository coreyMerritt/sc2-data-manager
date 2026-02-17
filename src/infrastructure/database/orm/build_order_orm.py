from typing import TYPE_CHECKING, ClassVar, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
  from infrastructure.database.orm.build_entry_orm import BuildEntryORM
  from infrastructure.database.orm.game_participant_orm import GameParticipantORM

class BuildOrderORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "build_order"
  id: int | None = Field(
    primary_key=True,
    unique=True,
    nullable=False,
    default=None
  )
  game_participant_id: int | None = Field(
    primary_key=False,
    unique=True,
    nullable=False,
    default=None,
    foreign_key="game_participant.id"
  )

  build_entries: List["BuildEntryORM"] = Relationship(back_populates="build_order")
  game_participant: "GameParticipantORM" = Relationship(back_populates="build_order")
