from typing import ClassVar, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
  from infrastructure.database.orm.build_order_orm import BuildOrderORM


class BuildEntryORM(SQLModel, table=True):
  __tablename__: ClassVar[str] = "build_entry"
  id: int | None = Field(
    primary_key=True,
    unique=True,
    nullable=False,
    default=None
  )
  build_order_id: int | None = Field(
    primary_key=False,
    unique=False,
    nullable=False,
    default=None,
    foreign_key="build_order.id"
  )

  item_name: str = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  supply: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  supply_total: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )
  timestamp: int = Field(
    primary_key=False,
    unique=False,
    nullable=False
  )

  build_order: "BuildOrderORM" = Relationship(back_populates="build_entries")
