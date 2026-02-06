from domain.subdomain.entities.user import User
from services.models.outputs.user.delete_user_som import DeleteUserSOM


class DeleteUserMapper:
  @staticmethod
  def entity_to_som(entity: User) -> DeleteUserSOM:
    return DeleteUserSOM(
      ulid=entity.ulid,
      email_address=entity.email_address,
      username=entity.username,
      user_type=entity.user_type
    )
