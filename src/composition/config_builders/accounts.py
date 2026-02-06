import os
import sys

from infrastructure.auth.models.accounts_config import AccountsConfig
from infrastructure.config.parser import ConfigParser
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.types.logger_interface import LoggerInterface


def build_final_accounts_config(
  config_parser: ConfigParser,
  logger: LoggerInterface
) -> AccountsConfig:
  accounts_config_dict = {}
  admin_secret_from_env_var = os.getenv(EnvVar.USERS_ADMIN_SECRET.value)
  if admin_secret_from_env_var is None:
    logger.critical(f"You must export {EnvVar.USERS_ADMIN_SECRET.value}", error=None)
    sys.exit(1)
  accounts_config_dict["admin_secret"] = os.getenv(EnvVar.USERS_ADMIN_SECRET.value)
  return config_parser.parse_accounts_config(accounts_config_dict)
