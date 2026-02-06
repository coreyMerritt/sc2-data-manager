from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.config.parser import ConfigParser
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.logger.models.logger_config import LoggerConfig
from infrastructure.types.logger_interface import LoggerInterface


def build_final_logger_config(
  config_parser: ConfigParser,
  logger: LoggerInterface | None,
  logger_config_dict: Dict[str, Any]
) -> LoggerConfig:
  _ = config_parser.parse_logger_config(logger_config_dict)
  logger_config_dict["level"] = get_final_config_var(
    logger=logger,
    config_var=logger_config_dict["level"],
    env_var=EnvVar.LOGGER_LEVEL
  )
  logger_config_dict["timezone"] = get_final_config_var(
    logger=logger,
    config_var=logger_config_dict["timezone"],
    env_var=EnvVar.LOGGER_TIMEZONE
  )
  logger_config_dict["json"] = get_final_config_var(
    logger=logger,
    config_var=logger_config_dict["json"],
    env_var=EnvVar.LOGGER_JSON
  )
  return config_parser.parse_logger_config(logger_config_dict)
