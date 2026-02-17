from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import col, delete, select, update

from domain.exceptions.repository_duplication_err import RepositoryDuplicationErr
from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from infrastructure.database.database import Database
from infrastructure.database.orm.game_summary_orm import GameSummaryORM


class GameSummaryRepository:
  _database: Database

  def __init__(self, database: Database):
    self._database = database

  def exists(self, filehash: str) -> bool:
    try:
      with self._database.get_session() as session:
        select_statement = select(GameSummaryORM).where(
          GameSummaryORM.filehash == filehash
        )
        first_game_summary_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_game_summary_orm_match is None:
      return False
    return True

  def create(self, game_summary_orm: GameSummaryORM) -> GameSummaryORM:
    with self._database.get_session() as session:
      try:
        session.add(game_summary_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(game_summary_orm)  # Fetch the ORM from transaction -- give "game_summary_orm" id/timestamp/etc
        session.commit()
      except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e):
          raise RepositoryDuplicationErr() from e
        raise RepositoryUnavailableErr() from e
      except SQLAlchemyError as e:
        session.rollback()
        raise RepositoryUnavailableErr() from e
      return game_summary_orm

  def get(self, filehash: str) -> GameSummaryORM:
    try:
      with self._database.get_session() as session:
        select_statement = select(GameSummaryORM).where(
          GameSummaryORM.filehash == filehash
        )
        first_game_summary_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_game_summary_orm_match is None:
      raise RepositoryNotFoundErr()
    return first_game_summary_orm_match

  def delete(self, filehash: str) -> GameSummaryORM:
    game_summary_orm = self.get(filehash)
    try:
      with self._database.get_session() as session:
        select_statement = delete(GameSummaryORM).where(
          col(GameSummaryORM.filehash) == filehash
        )
        session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    return game_summary_orm
