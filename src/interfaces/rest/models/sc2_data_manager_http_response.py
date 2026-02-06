from typing import Generic, TypeVar

from pydantic import BaseModel

from interfaces.rest.models.sc2_data_manager_http_error import SC2DataManagerHTTPError

T = TypeVar("T", bound=BaseModel)

class SC2DataManagerHTTPResponse(BaseModel, Generic[T]):
  data: T | None = None
  error: SC2DataManagerHTTPError | None = None
