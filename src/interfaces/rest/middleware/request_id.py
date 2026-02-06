import ulid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
  def __init__(self, app):
    super().__init__(app)

  async def dispatch(self, request: Request, call_next):
    incoming_corr = request.headers.get("x-correlation-id")
    correlation_id = incoming_corr or ulid.new().str
    request_id = ulid.new().str
    request.state.correlation_id = correlation_id
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["x-correlation-id"] = correlation_id
    response.headers["x-request-id"] = request_id
    return response
