from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.config.parser import ConfigParser
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.memory.models.memory_config import MemoryConfig
from infrastructure.types.logger_interface import LoggerInterface


def build_final_memory_config(
  config_parser: ConfigParser,
  logger: LoggerInterface,
  memory_config_dict: Dict[str, Any]
) -> MemoryConfig:
  _ = config_parser.parse_memory_config(memory_config_dict)
  memory_config_dict["maximum_healthy_usage_percentage"] = get_final_config_var(
    logger=logger,
    config_var=memory_config_dict["maximum_healthy_usage_percentage"],
    env_var=EnvVar.MEMORY_MAXIMUM_HEALTHY_USAGE_PERCENTAGE
  )
  return config_parser.parse_memory_config(memory_config_dict)
