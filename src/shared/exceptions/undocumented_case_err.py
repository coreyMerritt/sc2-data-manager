from shared.exceptions.base_shared_exception import BaseSharedException


class UndocumentedCaseErr(BaseSharedException):
  message: str

  def __init__(self, *args):
    message="Encountered an case that has not been considered."
    self.message = message
    super().__init__(message, *args)
