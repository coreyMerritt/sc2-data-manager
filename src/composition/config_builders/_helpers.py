import os
from typing import TypeVar, cast

from infrastructure.environment.models.env_var import EnvVar
from infrastructure.types.logger_interface import LoggerInterface
from shared.exceptions.undocumented_case_err import UndocumentedCaseErr

T = TypeVar("T")

def get_final_config_var(
  logger: LoggerInterface | None,
  config_var: T,
  env_var: EnvVar
) -> T:
  override = os.getenv(env_var.value)
  if override is not None and override != "":
    if override[0] == "'" and override[-1] == "'":
      raise ValueError("Environment Variables must NOT be set with single quotes. Set with no quotes.")
    if isinstance(config_var, bool):
      return cast(T, override)
    if isinstance(config_var, int):
      return cast(T, int(override))
    if isinstance(config_var, float):
      return cast(T, float(override))
    if isinstance(config_var, str):
      return cast(T, str(override))
    raise UndocumentedCaseErr()
  if logger:
    logger.debug(f"No override found, using config file for: {env_var.value}")
  return config_var
