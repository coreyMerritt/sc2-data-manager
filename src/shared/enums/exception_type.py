from enum import Enum


class ExceptionType(str, Enum):
  DOMAIN = "domain"
  INFRASTRUCTURE = "infrastructure"
  INTERFACE = "interface"
  SHARED = "shared"
  SERVICE = "service"
