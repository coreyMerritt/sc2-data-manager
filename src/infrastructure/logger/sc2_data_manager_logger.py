import json
import sys
import traceback
from dataclasses import asdict
from datetime import datetime
from http import HTTPStatus
from zoneinfo import ZoneInfo

from rich.console import Console
from rich.traceback import Traceback
from rich.traceback import install as install_rich_tracebacks

from infrastructure.logger.enums.logger_level import LoggerLevel
from infrastructure.logger.exceptions.logger_initialization_err import LoggerInitializationErr
from infrastructure.logger.models.logger_config import LoggerConfig
from infrastructure.logger.models.logger_health_report import LoggerHealthReport
from infrastructure.logger.models.logs.base_log import BaseLog
from infrastructure.logger.models.logs.error import Error
from infrastructure.logger.models.logs.http_request_log import HTTPRequestLog
from infrastructure.logger.models.logs.http_response_log import HTTPResponseLog
from infrastructure.logger.models.logs.ids import IDs
from infrastructure.logger.models.logs.raw_http_request_info import RawHTTPRequestInfo
from infrastructure.logger.models.logs.raw_http_response_info import RawHTTPResponseInfo
from infrastructure.logger.models.logs.simple_log import SimpleLog
from infrastructure.logger.models.logs.status import Status
from infrastructure.logger.models.logs.timestamps import Timestamps
from infrastructure.types.logger_interface import LoggerInterface
from shared.exceptions.undocumented_case_err import UndocumentedCaseErr


class SC2DataManagerLogger(LoggerInterface):
  _console: Console
  _json: bool
  _level: LoggerLevel
  _zoneinfo: ZoneInfo

  def __init__(self, logger_config: LoggerConfig):
    try:
      if not logger_config.json:
        install_rich_tracebacks()
      self._console = Console(force_terminal=True)
      self._json = logger_config.json
      self._level = logger_config.level
      self._zoneinfo = ZoneInfo(logger_config.timezone.value)
      super().__init__()
    except Exception as e:
      raise LoggerInitializationErr() from e

  def set_json(self, is_json: bool) -> None:
    self._json = is_json

  def set_level(self, level: LoggerLevel) -> None:
    self._level = level

  def get_health_report(self) -> LoggerHealthReport:
    return LoggerHealthReport(
      healthy=True
    )

####################### Simple Logging Methods #######################

  def debug(
    self,
    message: str
  ) -> None:
    if self._level not in (
      LoggerLevel.DEBUG
    ):
      return
    level = "DEBUG"
    log = self._get_simple_log(message, level, None)
    self._print_log(log, None)

  def info(
    self,
    message: str
  ) -> None:
    if self._level not in (
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "INFO"
    log = self._get_simple_log(message, level, None)
    self._print_log(log, None)

  def warning(
    self,
    message: str,
    error: Exception | None
  ) -> None:
    if self._level not in (
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "WARNING"
    log = self._get_simple_log(message, level, error)
    self._print_log(log, error)

  def error(
    self,
    message: str,
    error: Exception | None
  ) -> None:
    if self._level not in (
      LoggerLevel.ERROR,
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "ERROR"
    log = self._get_simple_log(message, level, error)
    self._print_log(log, error)

  def critical(
    self,
    message: str,
    error: Exception | None
  ) -> None:
    if self._level not in (
      LoggerLevel.CRITICAL,
      LoggerLevel.ERROR,
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "CRITICAL"
    log = self._get_simple_log(message, level, error)
    self._print_log(log, error)

####################### HTTP Request Logging Methods #######################

  def http_req_debug(
    self,
    message: str,
    raw_http_req_info: RawHTTPRequestInfo
  ) -> None:
    if self._level not in (
      LoggerLevel.DEBUG
    ):
      return
    level = "DEBUG"
    log = self._build_http_request_log(message, level, None, raw_http_req_info)
    self._print_log(log, None)

  def http_req_info(
    self,
    message: str,
    raw_http_req_info: RawHTTPRequestInfo
  ) -> None:
    if self._level not in (
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "INFO"
    log = self._build_http_request_log(message, level, None, raw_http_req_info)
    self._print_log(log, None)

  def http_req_warning(
    self,
    message: str,
    error: Exception | None,
    raw_http_req_info: RawHTTPRequestInfo
  ) -> None:
    if self._level not in (
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "WARNING"
    log = self._build_http_request_log(message, level, error, raw_http_req_info)
    self._print_log(log, error)

  def http_req_error(
    self,
    message: str,
    error: Exception | None,
    raw_http_req_info: RawHTTPRequestInfo
  ) -> None:
    if self._level not in (
      LoggerLevel.ERROR,
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "ERROR"
    log = self._build_http_request_log(message, level, error, raw_http_req_info)
    self._print_log(log, error)

  def http_req_critical(
    self,
    message: str,
    error: Exception | None,
    raw_http_req_info: RawHTTPRequestInfo
  ) -> None:
    if self._level not in (
      LoggerLevel.CRITICAL,
      LoggerLevel.ERROR,
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "CRITICAL"
    log = self._build_http_request_log(message, level, error, raw_http_req_info)
    self._print_log(log, error)

####################### HTTP Response Logging Methods #######################

  def http_res_debug(
    self,
    message: str,
    raw_http_res_info: RawHTTPResponseInfo
  ) -> None:
    if self._level not in (
      LoggerLevel.DEBUG
    ):
      return
    level = "DEBUG"
    log = self._build_http_response_log(message, level, None, raw_http_res_info)
    self._print_log(log, None)

  def http_res_info(
    self,
    message: str,
    raw_http_res_info: RawHTTPResponseInfo
  ) -> None:
    if self._level not in (
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "INFO"
    log = self._build_http_response_log(message, level, None, raw_http_res_info)
    self._print_log(log, None)

  def http_res_warning(
    self,
    message: str,
    error: Exception | None,
    raw_http_res_info: RawHTTPResponseInfo
  ) -> None:
    if self._level not in (
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "WARNING"
    log = self._build_http_response_log(message, level, error, raw_http_res_info)
    self._print_log(log, error)

  def http_res_error(
    self,
    message: str,
    error: Exception | None,
    raw_http_res_info: RawHTTPResponseInfo
  ) -> None:
    if self._level not in (
      LoggerLevel.ERROR,
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "ERROR"
    log = self._build_http_response_log(message, level, error, raw_http_res_info)
    self._print_log(log, error)

  def http_res_critical(
    self,
    message: str,
    error: Exception | None,
    raw_http_res_info: RawHTTPResponseInfo
  ) -> None:
    if self._level not in (
      LoggerLevel.CRITICAL,
      LoggerLevel.ERROR,
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "CRITICAL"
    log = self._build_http_response_log(message, level, error, raw_http_res_info)
    self._print_log(log, error)

####################### Private Methods #######################

  def _get_simple_log(self, message: str, level: str, error: Exception | None) -> SimpleLog:
    timestamps = self._build_timestamps()
    log_error = self._build_error(error)
    return SimpleLog(
      message=message,
      level=level,
      timestamps=timestamps,
      error=log_error
    )

  def _build_http_request_log(
    self,
    message: str,
    level: str,
    error: Exception | None,
    raw_http_request_info: RawHTTPRequestInfo
  ) -> HTTPRequestLog:
    log_error = self._build_error(error)
    log_ids = self._build_ids(
      correlation_id=raw_http_request_info.correlation_id,
      request_id=raw_http_request_info.request_id
    )
    timestamps = self._build_timestamps()
    return HTTPRequestLog(
      message=message,
      level=level,
      timestamps=timestamps,
      error=log_error,
      ids=log_ids,
      client_ip=raw_http_request_info.client_ip,
      endpoint=raw_http_request_info.endpoint,
      method=raw_http_request_info.method,
      route=raw_http_request_info.route,
      user_agent=raw_http_request_info.user_agent
    )

  def _build_http_response_log(
    self,
    message: str,
    level: str,
    error: Exception | None,
    raw_http_response_info: RawHTTPResponseInfo
  ) -> HTTPResponseLog:
    log_error = self._build_error(error)
    ids = self._build_ids(
      correlation_id=raw_http_response_info.correlation_id,
      request_id=raw_http_response_info.request_id
    )
    status = self._build_status(raw_http_response_info.status)
    timestamps = self._build_timestamps()
    return HTTPResponseLog(
      message=message,
      level=level,
      timestamps=timestamps,
      error=log_error,
      ids=ids,
      status=status,
      duration_ms=raw_http_response_info.duration_ms
    )

  def _build_ids(self, correlation_id: str, request_id: str) -> IDs:
    return IDs(
      correlation_id=correlation_id,
      request_id=request_id
    )

  def _build_error(self, exception: Exception | None) -> Error | None:
    if not exception:
      return None
    return Error(
      name=type(exception).__name__,
      message=str(exception),
      stack="".join(traceback.format_exception(exception)).replace("\n", "\\n")
    )

  def _build_status(self, status: int) -> Status:
    http_status = HTTPStatus(status)
    return Status(
      code=http_status.value,
      name=http_status.name
    )

  def _build_timestamps(self) -> Timestamps:
    now = datetime.now(self._zoneinfo)
    human_timestamp = self._get_human_timestamp(now)
    machine_timestamp = self._get_machine_timestamp(now)
    return Timestamps(
      human=human_timestamp,
      machine=machine_timestamp
    )

  def _get_human_timestamp(self, now: datetime) -> str:
    return now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond / 1000):03d}"

  def _get_machine_timestamp(self, now: datetime) -> str:
    return now.isoformat()

  def _print_log(self, log: BaseLog, err: Exception | None) -> None:
    if self._json:
      print(json.dumps(asdict(log), indent=2))
    else:
      self._print_human_log(log, err)
    sys.stdout.flush()

  def _print_human_log(self, log: BaseLog, err: Exception | None) -> None:
    if isinstance(log, SimpleLog):
      self._print_human_simple_log(log)
    elif isinstance(log, HTTPRequestLog):
      self._print_human_http_req_log(log)
    elif isinstance(log, HTTPResponseLog):
      self._print_human_http_res_log(log)
    else:
      raise UndocumentedCaseErr()
    if err:
      print()
      self._console.print(Traceback.from_exception(type(err), err, err.__traceback__))
    print("─" * 120)
    sys.stdout.flush()

  def _print_human_simple_log(self, simple_log: SimpleLog) -> None:
    level = self._get_colored_logger_level_tag(simple_log.level)
    print(f"     Timestamp: {simple_log.timestamps.human}")
    print(f"         Level: {level}")
    print(f"       Message: {simple_log.message}")


  def _print_human_http_req_log(self, http_req_log: HTTPRequestLog) -> None:
    level = self._get_colored_logger_level_tag(http_req_log.level)
    print(f"     Timestamp: {http_req_log.timestamps.human}")
    print(f"         Level: {level}")
    print(f"       Message: {http_req_log.message}")
    print(f"    Request ID: {http_req_log.ids.request_id}")
    print(f"Correlation ID: {http_req_log.ids.correlation_id}")
    print(f"     Client IP: {http_req_log.client_ip}")
    print(f"        Method: {http_req_log.method}")
    print(f"      Endpoint: {http_req_log.endpoint}")
    print(f"    User Agent: {http_req_log.user_agent}")

  def _print_human_http_res_log(self, http_res_log: HTTPResponseLog) -> None:
    level = self._get_colored_logger_level_tag(http_res_log.level)
    print(f"     Timestamp: {http_res_log.timestamps.human}")
    print(f"         Level: {level}")
    print(f"       Message: {http_res_log.message}")
    print(f"    Request ID: {http_res_log.ids.request_id}")
    print(f"Correlation ID: {http_res_log.ids.correlation_id}")
    print(f"   Status Code: {http_res_log.status.code}")
    print(f"   Status Name: {http_res_log.status.name}")
    print(f" Duration (ms): {http_res_log.duration_ms}")

  def _get_colored_logger_level_tag(self, logger_level: str) -> str:
    ll = logger_level.lower()
    if ll == "debug":
      return logger_level
    if ll == "info":
      return f"\033[38;2;91;91;255m{logger_level}\033[0m"
    if ll == "warning":
      return f"\033[38;2;255;255;0m{logger_level}\033[0m"
    if ll == "error":
      return f"\033[38;2;255;128;0m{logger_level}\033[0m"
    if ll == "critical":
      return f"\033[38;2;255;0;0m{logger_level}\033[0m"
    raise UndocumentedCaseErr()
