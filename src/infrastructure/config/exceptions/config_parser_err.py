from infrastructure.exceptions.infrastructure_exception import BaseInfrastructureException


class ConfigParserErr(BaseInfrastructureException):
  config_name: str
  message: str

  def __init__(self, config_name: str, *args):
    message=f"Failed to parse configuration: {config_name}"
    self.config_name = config_name
    self.message = message
    super().__init__(message, *args)
