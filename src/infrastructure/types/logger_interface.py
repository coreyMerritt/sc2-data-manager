from typing import Protocol

from infrastructure.logger.enums.logger_level import LoggerLevel
from infrastructure.logger.models.logger_health_report import LoggerHealthReport
from infrastructure.logger.models.logs.raw_http_request_info import RawHTTPRequestInfo
from infrastructure.logger.models.logs.raw_http_response_info import RawHTTPResponseInfo


class LoggerInterface(Protocol):
  def get_health_report(self) -> LoggerHealthReport: ...
  def debug(
    self,
    message: str
  ) -> None: ...
  def info(
    self,
    message: str
  ) -> None: ...
  def warning(
    self,
    message: str,
    error: Exception | None
  ) -> None: ...
  def error(
    self,
    message: str,
    error: Exception | None
  ) -> None: ...
  def critical(
    self,
    message: str,
    error: Exception | None
  ) -> None: ...
  def http_req_debug(
    self,
    message: str,
    raw_http_req_info: RawHTTPRequestInfo
  ) -> None: ...
  def http_req_info(
    self,
    message: str,
    raw_http_req_info: RawHTTPRequestInfo
  ) -> None: ...
  def http_req_warning(
    self,
    message: str,
    error: Exception | None,
    raw_http_req_info: RawHTTPRequestInfo
  ) -> None: ...
  def http_req_error(
    self,
    message: str,
    error: Exception | None,
    raw_http_req_info: RawHTTPRequestInfo
  ) -> None: ...
  def http_req_critical(
    self,
    message: str,
    error: Exception | None,
    raw_http_req_info: RawHTTPRequestInfo
  ) -> None: ...
  def http_res_debug(
    self,
    message: str,
    raw_http_res_info: RawHTTPResponseInfo
  ) -> None: ...
  def http_res_info(
    self,
    message: str,
    raw_http_res_info: RawHTTPResponseInfo
  ) -> None: ...
  def http_res_warning(
    self,
    message: str,
    error: Exception | None,
    raw_http_res_info: RawHTTPResponseInfo
  ) -> None: ...
  def http_res_error(
    self,
    message: str,
    error: Exception | None,
    raw_http_res_info: RawHTTPResponseInfo
  ) -> None: ...
  def http_res_critical(
    self,
    message: str,
    error: Exception | None,
    raw_http_res_info: RawHTTPResponseInfo
  ) -> None: ...
  def set_json(self, is_json: bool) -> None: ...
  def set_level(self, level: LoggerLevel) -> None: ...
