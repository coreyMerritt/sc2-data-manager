from dataclasses import dataclass


@dataclass
class RawHTTPResponseInfo:
  correlation_id: str
  request_id: str
  duration_ms: float
  status: int
