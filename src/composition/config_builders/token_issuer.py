from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.auth.models.token_issuer_config import TokenIssuerConfig
from infrastructure.config.parser import ConfigParser
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.types.logger_interface import LoggerInterface


def build_final_token_issuer_config(
  config_parser: ConfigParser,
  logger: LoggerInterface,
  token_issuer_config_dict: Dict[str, Any]
) -> TokenIssuerConfig:
  _ = config_parser.parse_token_issuer_config(token_issuer_config_dict)
  token_issuer_config_dict["time_to_live_days"] = get_final_config_var(
    logger=logger,
    config_var=token_issuer_config_dict["time_to_live_days"],
    env_var=EnvVar.TOKEN_ISSUER_TIME_TO_LIVE_DAYS
  )
  return config_parser.parse_token_issuer_config(token_issuer_config_dict)
