from infrastructure.exceptions.infrastructure_exception import BaseInfrastructureException


class DatabaseSchemaCreationErr(BaseInfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to create database schema."
    self.message = message
    super().__init__(message, *args)
