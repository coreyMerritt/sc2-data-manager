from interfaces.rest.v1.dto.res.user.delete_user_res import DeleteUserRes
from services.models.outputs.user.delete_user_som import DeleteUserSOM


class DeleteUserMapper:
  @staticmethod
  def som_to_res(som: DeleteUserSOM) -> DeleteUserRes:
    return DeleteUserRes(
      ulid=som.ulid,
      username=som.username,
      email_address=som.email_address,
      user_type=som.user_type
    )
