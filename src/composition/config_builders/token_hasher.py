import os
import sys

from infrastructure.auth.models.token_hasher_config import TokenHasherConfig
from infrastructure.config.parser import ConfigParser
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.types.logger_interface import LoggerInterface


def build_final_token_hasher_config(
  config_parser: ConfigParser,
  logger: LoggerInterface
) -> TokenHasherConfig:
  token_hasher_config_dict = {}
  secret_from_env_var = os.getenv(EnvVar.TOKEN_HASHER_SECRET.value)
  if secret_from_env_var is None:
    logger.critical(f"You must export {EnvVar.TOKEN_HASHER_SECRET.value}", error=None)
    sys.exit(1)
  token_hasher_config_dict["secret"] = os.getenv(EnvVar.TOKEN_HASHER_SECRET.value)
  return config_parser.parse_token_hasher_config(token_hasher_config_dict)
