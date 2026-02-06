from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.config.parser import ConfigParser
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.types.logger_interface import LoggerInterface
from infrastructure.uvicorn.models.uvicorn_config import UvicornConfig


def build_final_uvicorn_config(
  config_parser: ConfigParser,
  logger: LoggerInterface,
  uvicorn_config_dict: Dict[str, Any]
) -> UvicornConfig:
  _ = config_parser.parse_uvicorn_config(uvicorn_config_dict)
  uvicorn_config_dict["access_log"] = get_final_config_var(
    logger=logger,
    config_var=uvicorn_config_dict["access_log"],
    env_var=EnvVar.UVICORN_ACCESS_LOG
  )
  uvicorn_config_dict["app"] = get_final_config_var(
    logger=logger,
    config_var=uvicorn_config_dict["app"],
    env_var=EnvVar.UVICORN_APP
  )
  uvicorn_config_dict["factory"] = get_final_config_var(
    logger=logger,
    config_var=uvicorn_config_dict["factory"],
    env_var=EnvVar.UVICORN_FACTORY
  )
  uvicorn_config_dict["host"] = get_final_config_var(
    logger=logger,
    config_var=uvicorn_config_dict["host"],
    env_var=EnvVar.UVICORN_HOST
  )
  uvicorn_config_dict["log_config"] = get_final_config_var(
    logger=logger,
    config_var=uvicorn_config_dict["log_config"],
    env_var=EnvVar.UVICORN_LOG_CONFIG
  )
  uvicorn_config_dict["port"] = get_final_config_var(
    logger=logger,
    config_var=uvicorn_config_dict["port"],
    env_var=EnvVar.UVICORN_PORT
  )
  uvicorn_config_dict["reload"] = get_final_config_var(
    logger=logger,
    config_var=uvicorn_config_dict["reload"],
    env_var=EnvVar.UVICORN_RELOAD
  )
  uvicorn_config_dict["server_header"] = get_final_config_var(
    logger=logger,
    config_var=uvicorn_config_dict["server_header"],
    env_var=EnvVar.UVICORN_SERVER_HEADER
  )
  return config_parser.parse_uvicorn_config(uvicorn_config_dict)
