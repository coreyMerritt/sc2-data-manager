from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import col, delete, select, update

from domain.exceptions.repository_duplication_err import RepositoryDuplicationErr
from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from infrastructure.database.database import Database
from infrastructure.database.orm.account_orm import AccountORM


class AccountRepository:
  _database: Database

  def __init__(self, database: Database):
    self._database = database

  def exists(self, bnetid: int, region: str) -> bool:
    try:
      with self._database.get_session() as session:
        select_statement = select(AccountORM).where(
          col(AccountORM.bnetid) == bnetid,
          col(AccountORM.region) == region
        )
        first_account_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_account_orm_match is None:
      return False
    return True

  def create(self, account_orm: AccountORM) -> AccountORM:
    with self._database.get_session() as session:
      try:
        session.add(account_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(account_orm)  # Fetch the ORM from transaction -- give "account_orm" id/timestamp/etc
        session.commit()
      except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e):
          raise RepositoryDuplicationErr() from e
        raise RepositoryUnavailableErr() from e
      except SQLAlchemyError as e:
        session.rollback()
        raise RepositoryUnavailableErr() from e
      return account_orm

  def get(self, bnetid: int, region: str) -> AccountORM:
    try:
      with self._database.get_session() as session:
        select_statement = select(AccountORM).where(
          col(AccountORM.bnetid) == bnetid,
          col(AccountORM.region) == region
        )
        first_account_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_account_orm_match is None:
      raise RepositoryNotFoundErr()
    return first_account_orm_match

  def delete(self, bnetid: int, region: str) -> AccountORM:
    account_orm = self.get(bnetid, region)
    try:
      with self._database.get_session() as session:
        select_statement = delete(AccountORM).where(
          col(AccountORM.bnetid) == bnetid,
          col(AccountORM.region) == region
        )
        session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    return account_orm
