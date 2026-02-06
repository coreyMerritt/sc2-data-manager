from urllib.parse import quote_plus

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine, text

from infrastructure.base_infrastructure import BaseInfrastructure
from infrastructure.database.exceptions.database_initialization_err import DatabaseInitializationErr
from infrastructure.database.exceptions.database_schema_creation_err import DatabaseSchemaCreationErr
from infrastructure.database.models.database_config import DatabaseConfig
from infrastructure.database.models.database_health_report import DatabaseHealthReport


class Database(BaseInfrastructure):
  _engine: Engine
  _session_factory: sessionmaker

  def __init__(self, database_config: DatabaseConfig):
    try:
      engine_str = database_config.engine
      if engine_str == "postgresql":
        engine_str = f"{engine_str}+psycopg"
      username = database_config.username
      password = quote_plus(database_config.password)
      host = database_config.host
      port = database_config.port
      name = database_config.name
      self._engine = create_engine(
        f"{engine_str}://{username}:{password}@{host}:{port}/{name}",
        connect_args={"connect_timeout": 5}
      )
      self._session_factory = sessionmaker(bind=self._engine, future=True, expire_on_commit=False)
      if not getattr(self._engine, "_schema_initialized", False):
        self.create_schema()
        setattr(self._engine, "_schema_initialized", True)
      assert self.can_perform_basic_select()
      super().__init__()
    except Exception as e:
      raise DatabaseInitializationErr() from e

  def can_perform_basic_select(self) -> bool:
    try:
      with self._engine.connect() as conn:
        conn.execute(text("SELECT 1"))
      return True
    except SQLAlchemyError:
      return False

  def get_health_report(self) -> DatabaseHealthReport:
    can_perform_basic_select = self.can_perform_basic_select()
    is_engine = self.get_engine() is not None
    is_session_factory = self.get_session_factory() is not None
    healthy = can_perform_basic_select and is_engine and is_session_factory
    return DatabaseHealthReport(
      can_perform_basic_select=can_perform_basic_select,
      is_engine=is_engine,
      is_session_factory=is_session_factory,
      healthy=healthy
    )

  def get_engine(self) -> Engine:
    return self._engine

  def get_session(self) -> Session:
    return Session(self._engine)

  def get_session_factory(self) -> sessionmaker:
    return self._session_factory

  def create_schema(self) -> None:
    try:
      SQLModel.metadata.create_all(self._engine)
    except SQLAlchemyError as e:
      raise DatabaseSchemaCreationErr() from e

  def dispose(self) -> None:
    self._engine.dispose()
