from fastapi import FastAPI

from interfaces.rest.middleware.auth import AuthMiddleware
from interfaces.rest.middleware.request_id import RequestIDMiddleware
from interfaces.rest.middleware.request_logging import RequestLoggingMiddleware
from interfaces.rest.middleware.response_logging import ResponseLoggingMiddleware
from services.user_manager import UserManager


def register_middleware(app: FastAPI) -> FastAPI:
  app.add_middleware(
    AuthMiddleware,
    get_authenticator=lambda: app.state.resources.infra.authenticator,
    get_logger=lambda: app.state.resources.infra.logger,
    get_user_manager=lambda: UserManager(
      user_admin_secret=app.state.resources.vars.users_admin_secret,
      logger=app.state.resources.infra.logger,
      password_hasher=app.state.resources.infra.password_hasher,
      user_repository=app.state.resources.repos.user
    )
  )
  app.add_middleware(
    ResponseLoggingMiddleware,
    get_logger=lambda: app.state.resources.infra.logger
  )
  app.add_middleware(
    RequestLoggingMiddleware,
    get_logger=lambda: app.state.resources.infra.logger
  )
  app.add_middleware(RequestIDMiddleware)
  return app
