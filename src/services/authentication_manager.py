from domain.interfaces.repositories.user_repository_interface import UserRepositoryInterface
from infrastructure.auth.password_verifier import PasswordVerifier
from infrastructure.auth.token_issuer import TokenIssuer
from infrastructure.types.logger_interface import LoggerInterface
from services.base_service import BaseService
from services.exceptions.invalid_credentials_err import InvalidCredentialsErr
from services.mappers.auth.create_token_mapper import CreateTokenMapper
from services.models.inputs.auth.create_token_sim import CreateTokenSIM
from services.models.outputs.auth.create_token_som import CreateTokenSOM


class AuthenticationManager(BaseService):
  _user_repository: UserRepositoryInterface
  _password_verifier: PasswordVerifier
  _token_issuer: TokenIssuer

  def __init__(
    self,
    logger: LoggerInterface,
    user_repository: UserRepositoryInterface,
    password_verifier: PasswordVerifier,
    token_issuer: TokenIssuer,
  ):
    self._user_repository = user_repository
    self._password_verifier = password_verifier
    self._token_issuer = token_issuer
    super().__init__(logger)

  def create_token(self, sim: CreateTokenSIM) -> CreateTokenSOM:
    self._logger.debug("Attempting authentication")
    try:
      user = self._user_repository.get_by_username(sim.username)
      if not self._password_verifier.verify(
        plaintext=sim.password,
        hashed=user.password_hash,
      ):
        self._logger.warning("Authentication failed: invalid credentials", error=None)
        raise InvalidCredentialsErr()
      token = self._token_issuer.issue(
        user_ulid=user.ulid
      )
      self._logger.debug(f"Issued auth token for user {user.ulid}")
    except InvalidCredentialsErr as e:
      raise e
    except Exception as e:
      self._raise_service_exception(e)
    return CreateTokenMapper.token_to_som(token)
