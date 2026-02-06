from interfaces.command_line.exceptions.base_interface_exception import BaseInterfaceException


class UnknownRunTargetException(BaseInterfaceException):
  message: str

  def __init__(self, *args):
    message="Unknown \"run\" target."
    self.message = message
    super().__init__(message, *args)
