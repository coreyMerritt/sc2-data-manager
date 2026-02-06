from interfaces.rest.v1.dto.req.user.create_user_req import CreateUserReq
from interfaces.rest.v1.dto.res.user.create_user_res import CreateUserRes
from services.models.inputs.user.create_user_sim import CreateUserSIM
from services.models.outputs.user.create_user_som import CreateUserSOM


class CreateUserMapper:
  @staticmethod
  def req_to_sim(req: CreateUserReq) -> CreateUserSIM:
    return CreateUserSIM(
      username=req.username,
      password=req.password,
      email_address=req.email_address,
      user_type=req.user_type,
      admin_secret=req.admin_secret
    )

  @staticmethod
  def som_to_res(som: CreateUserSOM) -> CreateUserRes:
    return CreateUserRes(
      ulid=som.ulid,
      username=som.username,
      email_address=som.email_address,
      user_type=som.user_type
    )
