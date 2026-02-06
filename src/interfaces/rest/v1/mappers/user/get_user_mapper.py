from interfaces.rest.v1.dto.res.user.get_user_res import GetUserRes
from services.models.outputs.user.get_user_som import GetUserSOM


class GetUserMapper:
  @staticmethod
  def som_to_res(som: GetUserSOM) -> GetUserRes:
    return GetUserRes(
      ulid=som.ulid,
      username=som.username,
      email_address=som.email_address,
      user_type=som.user_type
    )
