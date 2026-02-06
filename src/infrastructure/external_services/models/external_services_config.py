from dataclasses import dataclass


@dataclass(frozen=True)
class ExternalServicesConfig():
  request_timeout: float
