from fastapi import FastAPI, Request

from infrastructure.types.logger_interface import LoggerInterface
from interfaces.rest.exceptions.universal_exception_response import universal_exception_response
from services.exceptions.invalid_admin_secret_err import InvalidAdminSecretErr
from services.exceptions.invalid_credentials_err import InvalidCredentialsErr


def register_401_unauthorized_handlers(app: FastAPI) -> None:
  @app.exception_handler(InvalidAdminSecretErr)
  @app.exception_handler(InvalidCredentialsErr)
  async def handle_401(req: Request, exc: Exception):
    MESSAGE = "Unauthorized"
    CODE = 401
    logger: LoggerInterface = req.app.state.resources.infra.logger
    logger.warning(
      message=MESSAGE,
      error=exc
    )
    return await universal_exception_response(MESSAGE, CODE)
