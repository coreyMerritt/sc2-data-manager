from fastapi import FastAPI, Request

from infrastructure.types.logger_interface import LoggerInterface
from interfaces.rest.exceptions.universal_exception_response import universal_exception_response
from services.exceptions.item_not_found_err import ItemNotFoundErr


def register_404_not_found_handlers(app: FastAPI) -> None:
  @app.exception_handler(ItemNotFoundErr)
  async def handle_404(req: Request, exc: Exception):
    MESSAGE = "Not found"
    CODE = 404
    logger: LoggerInterface = req.app.state.resources.infra.logger
    logger.error(
      message=MESSAGE,
      error=exc
    )
    return await universal_exception_response(MESSAGE, CODE)
