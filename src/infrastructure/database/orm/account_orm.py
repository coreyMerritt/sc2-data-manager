from typing import ClassVar, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
  from .game_participant_orm import GameParticipantORM

class AccountORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "account"
  bnetid: int = Field(
    primary_key=True,
    unique=True,
    nullable=False
  )

  name: str | None = Field(
    primary_key=False,
    unique=False,
    nullable=True
  )

  game_participants: List["GameParticipantORM"] = Relationship(back_populates="account")
