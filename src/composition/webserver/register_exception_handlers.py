from fastapi import FastAPI

from interfaces.rest.exceptions.handlers._400_bad_request import register_400_bad_request_handlers
from interfaces.rest.exceptions.handlers._401_unauthorized import register_401_unauthorized_handlers
from interfaces.rest.exceptions.handlers._404_not_found import register_404_not_found_handlers
from interfaces.rest.exceptions.handlers._409_conflict import register_409_conflict_handlers
from interfaces.rest.exceptions.handlers._500_internal_server_error import register_500_internal_server_error_handlers
from interfaces.rest.exceptions.handlers.starlette_override import register_starlette_override


def register_exception_handlers(app: FastAPI) -> FastAPI:
  register_400_bad_request_handlers(app)
  register_401_unauthorized_handlers(app)
  register_404_not_found_handlers(app)
  register_409_conflict_handlers(app)
  register_500_internal_server_error_handlers(app)
  register_starlette_override(app)
  return app
