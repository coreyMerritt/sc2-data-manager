from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.config.parser import ConfigParser
from infrastructure.disk.models.disk_config import DiskConfig
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.types.logger_interface import LoggerInterface


def build_final_disk_config(
  config_parser: ConfigParser,
  logger: LoggerInterface,
  disk_config_dict: Dict[str, Any]
) -> DiskConfig:
  _ = config_parser.parse_disk_config(disk_config_dict)
  disk_config_dict["game_summary_files_directory"] = get_final_config_var(
    logger=logger,
    config_var=disk_config_dict["game_summary_files_directory"],
    env_var=EnvVar.GAME_SUMMARY_FILES_DIRECTORY
  )
  disk_config_dict["maximum_healthy_usage_percentage"] = get_final_config_var(
    logger=logger,
    config_var=disk_config_dict["maximum_healthy_usage_percentage"],
    env_var=EnvVar.DISK_MAXIMUM_HEALTHY_USAGE_PERCENTAGE
  )
  return config_parser.parse_disk_config(disk_config_dict)
