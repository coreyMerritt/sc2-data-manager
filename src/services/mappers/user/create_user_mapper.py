from domain.enums.user_type import UserType
from domain.subdomain.entities.user import User
from services.exceptions.invalid_admin_secret_err import InvalidAdminSecretErr
from services.exceptions.service_unavailable_err import ServiceUnavailableErr
from services.models.inputs.user.create_user_sim import CreateUserSIM
from services.models.outputs.user.create_user_som import CreateUserSOM


class CreateUserMapper:
  @staticmethod
  def sim_to_entity(sim: CreateUserSIM, password_hash: str, admin_secret: str | None) -> User:
    if (
      sim.admin_secret
      or sim.user_type in (UserType.ADMIN.value, UserType.READ_ONLY_CLIENT.value, UserType.WRITE_CLIENT.value)
    ):
      if not admin_secret or admin_secret != sim.admin_secret:
        raise InvalidAdminSecretErr()
    return User(
      username=sim.username,
      email_address=sim.email_address,
      password_hash=password_hash,
      user_type=UserType(sim.user_type),
      ulid=None,
      email_verified=None,
      created_at=None,
      disabled_at=None
    )

  @staticmethod
  def entity_to_som(entity: User) -> CreateUserSOM:
    if not entity.ulid:
      raise ServiceUnavailableErr()
    return CreateUserSOM(
      ulid=entity.ulid,
      email_address=entity.email_address,
      username=entity.username,
      password_hash=entity.password_hash,
      user_type=entity.user_type.value
    )
