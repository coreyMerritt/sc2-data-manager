from interfaces.rest.v1.dto.req.auth.create_token_req import CreateTokenReq
from interfaces.rest.v1.dto.res.auth.create_token_res import CreateTokenRes
from services.models.inputs.auth.create_token_sim import CreateTokenSIM
from services.models.outputs.auth.create_token_som import CreateTokenSOM


class CreateTokenMapper:
  @staticmethod
  def req_to_sim(req: CreateTokenReq) -> CreateTokenSIM:
    return CreateTokenSIM(
      username=req.username,
      password=req.password,
    )

  @staticmethod
  def som_to_res(som: CreateTokenSOM) -> CreateTokenRes:
    return CreateTokenRes(
      token=som.token,
    )
