from enum import Enum


class LoggerLevel(str, Enum):
  DEBUG = "debug"
  INFO = "info"
  WARNING = "warning"
  ERROR = "error"
  CRITICAL = "critical"
