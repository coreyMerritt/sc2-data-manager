import os

from infrastructure.base_infrastructure import BaseInfrastructure
from infrastructure.environment.exceptions.unset_environment_variable_err import UnsetEnvironmentVariableErr
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.environment.models.environment_health_report import EnvironmentHealthReport


class Environment(BaseInfrastructure):
  _first_call: bool

  def __init__(self):
    self._first_call = True
    super().__init__()

  def get_health_report(self) -> EnvironmentHealthReport:
    REQUIRED_ENV_VARS = [
      EnvVar.GLOBAL_CONFIG_DIR
    ]
    healthy = True
    for _, env_var in enumerate(REQUIRED_ENV_VARS):
      try:
        self.get_env_var(env_var.value)
      except Exception:
        healthy = False
    return EnvironmentHealthReport(
      healthy=healthy
    )

  def get_env_var(self, env_var_name: str) -> str:
    try:
      env_var = os.getenv(env_var_name)
      if env_var is None:
        raise TypeError("env_var is None")
      return env_var
    except Exception as e:
      raise UnsetEnvironmentVariableErr(
        env_var_name=env_var_name
      ) from e

  def set_env_var(self, env_var_name: str, var_value: str) -> None:
    os.environ[env_var_name] = var_value
