from http import HTTPStatus

from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException

from interfaces.rest.exceptions.universal_exception_response import universal_exception_response


def register_starlette_override(app):
  @app.exception_handler(StarletteHTTPException)
  async def starlette_http_exception_handler(request: Request, exception: StarletteHTTPException):
    _ = request
    status = HTTPStatus(exception.status_code)
    return await universal_exception_response(status.phrase, status.value)
