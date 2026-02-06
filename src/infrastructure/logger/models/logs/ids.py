from dataclasses import dataclass


@dataclass
class IDs:
  correlation_id: str
  request_id: str
