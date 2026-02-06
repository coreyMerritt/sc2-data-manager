from domain.interfaces.repositories.user_repository_interface import UserRepositoryInterface
from infrastructure.auth.password_hasher import PasswordHasher
from infrastructure.types.logger_interface import LoggerInterface
from services.base_service import BaseService
from services.mappers.user.create_user_mapper import CreateUserMapper
from services.mappers.user.delete_user_mapper import DeleteUserMapper
from services.mappers.user.get_user_mapper import GetUserMapper
from services.mappers.user.update_user_mapper import UpdateUserMapper
from services.models.inputs.user.create_user_sim import CreateUserSIM
from services.models.inputs.user.update_user_sim import UpdateUserSIM
from services.models.outputs.user.create_user_som import CreateUserSOM
from services.models.outputs.user.delete_user_som import DeleteUserSOM
from services.models.outputs.user.get_user_som import GetUserSOM
from services.models.outputs.user.update_user_som import UpdateUserSOM


class UserManager(BaseService):
  _admin_secret: str
  _password_hasher: PasswordHasher
  _user_repository: UserRepositoryInterface

  def __init__(
    self,
    user_admin_secret: str,
    logger: LoggerInterface,
    password_hasher: PasswordHasher,
    user_repository: UserRepositoryInterface
  ):
    self._admin_secret = user_admin_secret
    self._password_hasher = password_hasher
    self._user_repository = user_repository
    super().__init__(logger)

  def create_user(self, create_user_sim: CreateUserSIM) -> CreateUserSOM:
    self._logger.debug("Attempting to create user...")
    try:
      hashed_password = self._password_hasher.hash(create_user_sim.password)
      user = CreateUserMapper.sim_to_entity(
        sim=create_user_sim,
        password_hash=hashed_password,
        admin_secret=self._admin_secret
      )
      created_user = self._user_repository.create(user)
    except Exception as e:
      self._raise_service_exception(e)
    create_user_som = CreateUserMapper.entity_to_som(created_user)
    self._logger.debug(f"Successfully created user with ULID: {created_user.ulid}")
    return create_user_som

  def get_user(self, ulid: str) -> GetUserSOM:
    self._logger.debug(f"Attempting to retrieve user with ULID: {ulid}")
    try:
      user = self._user_repository.get(ulid)
    except Exception as e:
      self._raise_service_exception(e)
    get_user_som = GetUserMapper.entity_to_som(user)
    self._logger.debug(f"Successfully retrieved user with ULID: {ulid}")
    return get_user_som

  def update_user(self, update_user_sim: UpdateUserSIM) -> UpdateUserSOM:
    self._logger.debug("Attempting to update user...")
    pre_changes_user = self._user_repository.get(update_user_sim.ulid)
    user = UpdateUserMapper.sim_to_entity(pre_changes_user, update_user_sim, self._admin_secret)
    try:
      user = self._user_repository.update(user)
    except Exception as e:
      self._raise_service_exception(e)
    get_user_som = UpdateUserMapper.entity_to_som(user)
    self._logger.debug(f"Successfully retrieved user with ULID: {user.ulid}")
    return get_user_som

  def delete_user(self, ulid: str) -> DeleteUserSOM:
    self._logger.debug(f"Attempting to retrieve user with ULID: {ulid}")
    try:
      user = self._user_repository.delete(ulid)
    except Exception as e:
      self._raise_service_exception(e)
    delete_user_som = DeleteUserMapper.entity_to_som(user)
    self._logger.debug(f"Successfully retrieved user with ULID: {ulid}")
    return delete_user_som
