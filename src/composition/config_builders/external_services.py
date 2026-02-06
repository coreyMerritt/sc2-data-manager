from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.config.parser import ConfigParser
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.external_services.models.external_services_config import ExternalServicesConfig
from infrastructure.types.logger_interface import LoggerInterface


def build_final_external_services_config(
  config_parser: ConfigParser,
  logger: LoggerInterface,
  external_services_config_dict: Dict[str, Any]
) -> ExternalServicesConfig:
  _ = config_parser.parse_external_services_config(external_services_config_dict)
  external_services_config_dict["request_timeout"] = get_final_config_var(
    logger=logger,
    config_var=external_services_config_dict["request_timeout"],
    env_var=EnvVar.EXTERNAL_SERVICES_REQUEST_TIMEOUT
  )
  return config_parser.parse_external_services_config(external_services_config_dict)
