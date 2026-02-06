from dataclasses import dataclass


@dataclass
class RawHTTPRequestInfo:
  correlation_id: str
  request_id: str
  client_ip: str
  endpoint: str
  method: str
  route: str
  user_agent: str
