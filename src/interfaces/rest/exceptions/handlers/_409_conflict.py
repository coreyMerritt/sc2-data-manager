from fastapi import FastAPI, Request

from infrastructure.types.logger_interface import LoggerInterface
from interfaces.rest.exceptions.universal_exception_response import universal_exception_response
from services.exceptions.uniqueness_violation_err import UniquenessViolationErr


def register_409_conflict_handlers(app: FastAPI) -> None:
  @app.exception_handler(UniquenessViolationErr)
  async def handle_409(req: Request, exc: Exception):
    MESSAGE = "Conflict"
    CODE = 409
    logger: LoggerInterface = req.app.state.resources.infra.logger
    logger.error(
      message=MESSAGE,
      error=exc
    )
    return await universal_exception_response(MESSAGE, CODE)
