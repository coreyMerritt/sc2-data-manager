from fastapi import FastAPI, Request

from infrastructure.types.logger_interface import LoggerInterface
from interfaces.rest.exceptions.universal_exception_response import universal_exception_response
from services.exceptions.item_creation_err import ItemCreationErr
from services.exceptions.service_initialization_err import ServiceInitializationErr
from services.exceptions.service_unavailable_err import ServiceUnavailableErr


def register_500_internal_server_error_handlers(app: FastAPI) -> None:
  @app.exception_handler(Exception)
  @app.exception_handler(ItemCreationErr)
  @app.exception_handler(ServiceInitializationErr)
  @app.exception_handler(ServiceUnavailableErr)
  async def handle_500(req: Request, exc: Exception):
    MESSAGE = "Internal server error"
    CODE = 500
    logger: LoggerInterface = req.app.state.resources.infra.logger
    logger.error(
      message=f"[Caught Unhandled Exception] {MESSAGE}",
      error=exc
    )
    return await universal_exception_response(MESSAGE, CODE)
