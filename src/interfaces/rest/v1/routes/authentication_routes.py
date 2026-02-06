from fastapi import APIRouter, Request

from interfaces.rest.models.sc2_data_manager_http_response import SC2DataManagerHTTPResponse
from interfaces.rest.v1.controllers.authentication_controller import AuthenticationController
from interfaces.rest.v1.dto.req.auth.create_token_req import CreateTokenReq

controller = AuthenticationController()
router = APIRouter(prefix="/api/v1/auth")


@router.post(
  path="/token",
  response_model=SC2DataManagerHTTPResponse,
  status_code=201,
)
async def create_token(
  body: CreateTokenReq,
  req: Request
) -> SC2DataManagerHTTPResponse:
  return await controller.create_token(
    req=req,
    body=body,
  )
