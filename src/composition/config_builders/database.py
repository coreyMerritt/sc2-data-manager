from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.config.parser import ConfigParser
from infrastructure.database.models.database_config import DatabaseConfig
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.types.logger_interface import LoggerInterface


def build_final_database_config(
  config_parser: ConfigParser,
  logger: LoggerInterface,
  database_config_dict: Dict[str, Any]
) -> DatabaseConfig:
  _ = config_parser.parse_database_config(database_config_dict)
  database_config_dict["engine"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["engine"],
    env_var=EnvVar.DATABASE_ENGINE
  )
  database_config_dict["host"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["host"],
    env_var=EnvVar.DATABASE_HOST
  )
  database_config_dict["name"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["name"],
    env_var=EnvVar.DATABASE_NAME
  )
  database_config_dict["password"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["password"],
    env_var=EnvVar.DATABASE_PASSWORD
  )
  database_config_dict["port"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["port"],
    env_var=EnvVar.DATABASE_PORT
  )
  database_config_dict["username"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["username"],
    env_var=EnvVar.DATABASE_USERNAME
  )
  return config_parser.parse_database_config(database_config_dict)
