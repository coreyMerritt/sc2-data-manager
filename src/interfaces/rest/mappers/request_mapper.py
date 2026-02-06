from fastapi import Request

from infrastructure.logger.models.logs.raw_http_request_info import RawHTTPRequestInfo
from infrastructure.logger.models.logs.raw_http_response_info import RawHTTPResponseInfo


class RequestMapper:
  @staticmethod
  def to_raw_http_req_info(req: Request) -> RawHTTPRequestInfo:
    client = req.client
    client_ip = str(client.host) if client else ""
    route = req.scope.get("route")
    route_path = route.path if route else ""
    user_agent = req.headers.get("user-agent")
    user_agent = user_agent if user_agent else ""
    return RawHTTPRequestInfo(
      correlation_id=req.state.correlation_id,
      request_id=req.state.request_id,
      client_ip=client_ip,
      endpoint=f"{req.method} {req.url.path}",
      method=req.method,
      route=route_path,
      user_agent=user_agent
    )

  @staticmethod
  def to_raw_http_res_info(req: Request, status: int, duration_ms: float) -> RawHTTPResponseInfo:
    return RawHTTPResponseInfo(
      correlation_id=req.state.correlation_id,
      request_id=req.state.request_id,
      duration_ms=duration_ms,
      status=status
    )
