from typing import Any

from dacite import Config, from_dict

from infrastructure.auth.models.accounts_config import AccountsConfig
from infrastructure.auth.models.token_hasher_config import TokenHasherConfig
from infrastructure.auth.models.token_issuer_config import TokenIssuerConfig
from infrastructure.base_infrastructure import BaseInfrastructure
from infrastructure.config.exceptions.config_parser_err import ConfigParserErr
from infrastructure.config.models.config_parser_health_report import ConfigParserHealthReport
from infrastructure.cpu.models.cpu_config import CpuConfig
from infrastructure.database.models.database_config import DatabaseConfig
from infrastructure.disk.models.disk_config import DiskConfig
from infrastructure.external_services.models.external_services_config import ExternalServicesConfig
from infrastructure.logger.enums.logger_level import LoggerLevel
from infrastructure.logger.models.logger_config import LoggerConfig
from infrastructure.memory.models.memory_config import MemoryConfig
from infrastructure.uvicorn.models.uvicorn_config import UvicornConfig
from shared.enums.timezone import Timezone


class ConfigParser(BaseInfrastructure):
  _default_config: Config

  def __init__(self):
    self._default_config = Config(
      strict=True,
      type_hooks={
        bool: self._parse_bool,
        float: self._parse_float,
        int: self._parse_int,
        str: self._parse_str,
        LoggerLevel: LoggerLevel,
        Timezone: Timezone,
      }
    )
    super().__init__()

  def get_health_report(self) -> ConfigParserHealthReport:
    return ConfigParserHealthReport(
      healthy=True
    )

  def parse_accounts_config(self, some_data: Any) -> AccountsConfig:
    try:
      return from_dict(
        data_class=AccountsConfig,
        data=some_data,
        config=self._default_config
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Accounts Config"
      ) from e

  def parse_cpu_config(self, some_data: Any) -> CpuConfig:
    try:
      return from_dict(
        data_class=CpuConfig,
        data=some_data,
        config=self._default_config
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Cpu Config"
      ) from e

  def parse_database_config(self, some_data: Any) -> DatabaseConfig:
    try:
      return from_dict(
        data_class=DatabaseConfig,
        data=some_data,
        config=self._default_config
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Database Config"
      ) from e

  def parse_disk_config(self, some_data: Any) -> DiskConfig:
    try:
      return from_dict(
        data_class=DiskConfig,
        data=some_data,
        config=self._default_config
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Disk Config"
      ) from e

  def parse_external_services_config(self, some_data: Any) -> ExternalServicesConfig:
    try:
      return from_dict(
        data_class=ExternalServicesConfig,
        data=some_data,
        config=self._default_config
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="External Services Config"
      ) from e

  def parse_logger_config(self, some_data: Any) -> LoggerConfig:
    try:
      return from_dict(
        data_class=LoggerConfig,
        data=some_data,
        config=self._default_config
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Logger Config"
      ) from e

  def parse_memory_config(self, some_data: Any) -> MemoryConfig:
    try:
      return from_dict(
        data_class=MemoryConfig,
        data=some_data,
        config=self._default_config
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Memory Config"
      ) from e

  def parse_token_hasher_config(self, some_data: Any) -> TokenHasherConfig:
    try:
      return from_dict(
        data_class=TokenHasherConfig,
        data=some_data,
        config=self._default_config
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="TokenHasher Config"
      ) from e

  def parse_token_issuer_config(self, some_data: Any) -> TokenIssuerConfig:
    try:
      return from_dict(
        data_class=TokenIssuerConfig,
        data=some_data,
        config=self._default_config
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="TokenIssuer Config"
      ) from e

  def parse_uvicorn_config(self, some_data: Any) -> UvicornConfig:
    try:
      return from_dict(
        data_class=UvicornConfig,
        data=some_data,
        config=self._default_config
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Uvicorn Config"
      ) from e

  def _parse_bool(self, some_value: bool | float | int | str) -> bool:
    if isinstance(some_value, bool):
      return some_value
    if isinstance(some_value, int):
      if some_value == 1:
        return True
      if some_value == 0:
        return False
      raise ValueError(f"Unable to parse int to bool: {some_value}")
    if isinstance(some_value, str):
      if some_value.lower().strip() in ("true", "t", "1", "on", "yes", "y"):
        return True
      if some_value.lower().strip() in ("false", "f", "0", "off", "no", "n"):
        return False
      raise ValueError(f"Unable to parse string to bool: {some_value}")
    raise ValueError("Was given non-str, non-int and non-bool")

  def _parse_float(self, some_value: bool | float | int | str) -> float:
    return float(some_value)

  def _parse_int(self, some_value: bool | float | int | str) -> int:
    return int(some_value)

  def _parse_str(self, some_value: bool | float | int | str) -> str:
    return str(some_value)
