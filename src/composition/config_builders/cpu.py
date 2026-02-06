from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.models.cpu_config import CpuConfig
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.types.logger_interface import LoggerInterface


def build_final_cpu_config(
  config_parser: ConfigParser,
  logger: LoggerInterface,
  cpu_config_dict: Dict[str, Any]
) -> CpuConfig:
  _ = config_parser.parse_cpu_config(cpu_config_dict)
  cpu_config_dict["check_interval_seconds"] = get_final_config_var(
    logger=logger,
    config_var=cpu_config_dict["check_interval_seconds"],
    env_var=EnvVar.CPU_CHECK_INTERVAL_SECONDS
  )
  cpu_config_dict["maximum_healthy_usage_percentage"] = get_final_config_var(
    logger=logger,
    config_var=cpu_config_dict["maximum_healthy_usage_percentage"],
    env_var=EnvVar.CPU_MAXIMUM_HEALTHY_USAGE_PERCENTAGE
  )
  return config_parser.parse_cpu_config(cpu_config_dict)
