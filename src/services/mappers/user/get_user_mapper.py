from domain.subdomain.entities.user import User
from services.models.outputs.user.get_user_som import GetUserSOM


class GetUserMapper:
  @staticmethod
  def entity_to_som(entity: User) -> GetUserSOM:
    return GetUserSOM(
      ulid=entity.ulid,
      email_address=entity.email_address,
      username=entity.username,
      user_type=entity.user_type
    )
