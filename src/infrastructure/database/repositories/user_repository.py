from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import col, delete, select, update

from domain.exceptions.repository_duplication_err import RepositoryDuplicationErr
from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from domain.interfaces.repositories.user_repository_interface import UserRepositoryInterface
from domain.subdomain.entities.user import User
from infrastructure.database.database import Database
from infrastructure.database.mappers.user_mapper import UserMapper
from infrastructure.database.orm.user_orm import UserORM


class UserRepository(UserRepositoryInterface):
  _database: Database

  def __init__(self, database: Database):
    self._database = database

  def create(self, user: User) -> User:
    user_orm = UserMapper.domain_to_orm(user)
    with self._database.get_session() as session:
      try:
        session.add(user_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(user_orm)  # Fetch the ORM from transaction -- give "user_orm" id/timestamp/etc
        session.commit()
      except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e):
          raise RepositoryDuplicationErr() from e
        raise RepositoryUnavailableErr() from e
      except SQLAlchemyError as e:
        session.rollback()
        raise RepositoryUnavailableErr() from e
      user = UserMapper.orm_to_domain(user_orm)
      return user

  def get(self, ulid: str) -> User:
    try:
      with self._database.get_session() as session:
        select_statement = select(UserORM).where(
          UserORM.ulid == ulid
        )
        first_user_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_user_orm_match is None:
      raise RepositoryNotFoundErr()
    user_match = UserMapper.orm_to_domain(first_user_orm_match)
    return user_match

  def get_by_username(self, username: str) -> User:
    try:
      with self._database.get_session() as session:
        select_statement = select(UserORM).where(
          UserORM.username == username
        )
        first_user_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_user_orm_match is None:
      raise RepositoryNotFoundErr()
    user_match = UserMapper.orm_to_domain(first_user_orm_match)
    return user_match

  def update(self, user: User) -> User:
    try:
      with self._database.get_session() as session:
        update_statement = (
          update(UserORM)
          .where(col(UserORM.ulid) == user.ulid)
          .values(
            username=user.username,
            email_address=user.email_address,
            email_verified=user.email_verified,
            disabled_at=user.disabled_at,
          )
        )
        result = session.exec(update_statement)
        if result.rowcount == 0:
          raise RepositoryNotFoundErr()
        select_statement = select(UserORM).where(
          UserORM.ulid == user.ulid
        )
        first_user_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_user_orm_match is None:
      raise RepositoryNotFoundErr()
    return UserMapper.orm_to_domain(first_user_orm_match)

  def delete(self, ulid: str) -> User:
    user = self.get(ulid)
    try:
      with self._database.get_session() as session:
        select_statement = delete(UserORM).where(
          col(UserORM.ulid) == ulid
        )
        session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    return user
