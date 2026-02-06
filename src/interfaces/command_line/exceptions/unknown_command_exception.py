from interfaces.command_line.exceptions.base_interface_exception import BaseInterfaceException


class UnknownCommandException(BaseInterfaceException):
  message: str

  def __init__(self, *args):
    message="Unknown command."
    self.message = message
    super().__init__(message, *args)
