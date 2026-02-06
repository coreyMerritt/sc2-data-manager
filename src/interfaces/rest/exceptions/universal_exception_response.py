from typing import Any

from fastapi.responses import JSONResponse

from interfaces.rest.models.sc2_data_manager_http_error import SC2DataManagerHTTPError
from interfaces.rest.models.sc2_data_manager_http_response import SC2DataManagerHTTPResponse


async def universal_exception_response(
  message: str,
  code: int
) -> JSONResponse:
  response_model = SC2DataManagerHTTPResponse[Any](
    data=None,
    error=SC2DataManagerHTTPError(message=message)
  )
  return JSONResponse(
    status_code=code,
    content=response_model.model_dump(),
  )
