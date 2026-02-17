import time
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

from composition.config_builders.cpu import build_final_cpu_config
from composition.config_builders.database import build_final_database_config
from composition.config_builders.disk import build_final_disk_config
from composition.config_builders.external_services import build_final_external_services_config
from composition.config_builders.logger import build_final_logger_config
from composition.config_builders.memory import build_final_memory_config
from composition.config_builders.token_hasher import build_final_token_hasher_config
from composition.config_builders.token_issuer import build_final_token_issuer_config
from composition.config_builders.uvicorn import build_final_uvicorn_config
from composition.enums.config_filenames import ConfigFilenames
from infrastructure.auth.authenticator import Authenticator
from infrastructure.auth.models.token_hasher_config import TokenHasherConfig
from infrastructure.auth.models.token_issuer_config import TokenIssuerConfig
from infrastructure.auth.password_hasher import PasswordHasher
from infrastructure.auth.password_verifier import PasswordVerifier
from infrastructure.auth.token_hasher import TokenHasher
from infrastructure.auth.token_issuer import TokenIssuer
from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.cpu import Cpu
from infrastructure.cpu.models.cpu_config import CpuConfig
from infrastructure.database.database import Database
from infrastructure.database.exceptions.database_initialization_err import DatabaseInitializationErr
from infrastructure.database.models.database_config import DatabaseConfig
from infrastructure.database.repositories.account_repository import AccountRepository
from infrastructure.database.repositories.game_summary_repository import GameSummaryRepository
from infrastructure.database.repositories.user_repository import UserRepository
from infrastructure.disk.disk import Disk
from infrastructure.disk.models.disk_config import DiskConfig
from infrastructure.environment.environment import Environment
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.external_services.models.external_services_config import ExternalServicesConfig
from infrastructure.logger.sc2_data_manager_logger import SC2DataManagerLogger
from infrastructure.logger.models.logger_config import LoggerConfig
from infrastructure.memory.memory import Memory
from infrastructure.memory.models.memory_config import MemoryConfig
from infrastructure.types.logger_interface import LoggerInterface
from infrastructure.uvicorn.models.uvicorn_config import UvicornConfig


def get_uvicorn_config() -> UvicornConfig:
  load_dotenv()
  _temp_environment = Environment()
  _temp_config_parser = ConfigParser()
  config_dir = _build_config_dir(_temp_environment)
  _temp_disk = _build_temp_disk(
    config_dir=config_dir,
    config_parser=_temp_config_parser
  )
  _temp_logger = _build_logger(
    logger_config=_build_logger_config(
      config_dir=config_dir,
      config_parser=_temp_config_parser,
      disk=_temp_disk,
      temp_logger=None
    )
  )
  return _build_uvicorn_config(
    config_dir=config_dir,
    config_parser=_temp_config_parser,
    disk=_temp_disk,
    logger=_temp_logger
  )


def get_resources_dict() -> Dict[str, Any]:
  load_dotenv()
  _temp_environment = Environment()
  _temp_config_parser = ConfigParser()
  config_dir = _build_config_dir(_temp_environment)
  _temp_disk = _build_temp_disk(
    config_dir=config_dir,
    config_parser=_temp_config_parser
  )
  _temp_logger = _build_logger(
    logger_config=_build_logger_config(
      config_dir=config_dir,
      config_parser=_temp_config_parser,
      disk=_temp_disk,
      temp_logger=None
    )
  )
  configs_dict = _build_configs_dict(
    config_dir=config_dir,
    config_parser=_temp_config_parser,
    disk=_temp_disk,
    logger=_temp_logger
  )
  infra_dict = _build_infra_dict(
    configs_dict=configs_dict
  )
  repos_dict = _build_repos_dict(
    database=infra_dict["database"]
  )
  vars_dict = _build_vars_dict(
    environment=infra_dict["environment"]
  )
  return {
    "configs": configs_dict,
    "infra": infra_dict,
    "repos": repos_dict,
    "vars": vars_dict
  }

#################### Final Dict Builders ####################

def _build_config_dir(environment: Environment) -> str:
  return environment.get_env_var(EnvVar.GLOBAL_CONFIG_DIR.value)

def _build_configs_dict(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger: LoggerInterface
) -> Dict[str, Any]:
  token_hasher_config = _build_token_hasher_config(
    config_parser=config_parser,
    logger=logger
  )
  cpu_config = _build_cpu_config(
    config_dir=config_dir,
    config_parser=config_parser,
    disk=disk,
    logger=logger
  )
  database_config = _build_database_config(
    config_dir=config_dir,
    config_parser=config_parser,
    disk=disk,
    logger=logger
  )
  disk_config = _build_disk_config(
    config_dir=config_dir,
    config_parser=config_parser,
    temp_disk=disk,
    logger=logger
  )
  external_services_config = _build_external_services_config(
    config_dir=config_dir,
    config_parser=config_parser,
    disk=disk,
    logger=logger
  )
  logger_config = _build_logger_config(
    config_dir=config_dir,
    config_parser=config_parser,
    disk=disk,
    temp_logger=logger
  )
  memory_config = _build_memory_config(
    config_dir=config_dir,
    config_parser=config_parser,
    disk=disk,
    logger=logger
  )
  token_hasher_config = _build_token_hasher_config(
    config_parser=config_parser,
    logger=logger
  )
  token_issuer_config = _build_token_issuer_config(
    config_dir=config_dir,
    config_parser=config_parser,
    disk=disk,
    logger=logger
  )
  uvicorn_config = _build_uvicorn_config(
    config_dir=config_dir,
    config_parser=config_parser,
    disk=disk,
    logger=logger
  )
  return {
    "cpu": cpu_config,
    "database": database_config,
    "disk": disk_config,
    "external_services": external_services_config,
    "logger": logger_config,
    "memory": memory_config,
    "token_hasher": token_hasher_config,
    "token_issuer": token_issuer_config,
    "uvicorn": uvicorn_config
  }

def _build_infra_dict(configs_dict: Dict[str, Any]) -> Dict[str, Any]:
  config_parser = ConfigParser()
  environment = Environment()
  # Build these first because they're dependencies
  logger = _build_logger(
    logger_config=configs_dict["logger"]
  )
  disk = _build_disk(
    disk_config=configs_dict["disk"]
  )
  database = _build_database(
    database_config=configs_dict["database"],
    logger=logger
  )
  token_hasher = _build_token_hasher(
    token_hasher_config=configs_dict["token_hasher"]
  )
  # All other Infra
  authenticator = _build_authenticator(
    database=database,
    token_hasher=token_hasher
  )
  cpu = _build_cpu(
    cpu_config=configs_dict["cpu"]
  )
  memory = _build_memory(
    memory_config=configs_dict["memory"]
  )
  password_hasher = _build_password_hasher()
  password_verifier = _build_password_verifier()
  token_issuer = _build_token_issuer(
    token_issuer_config=configs_dict["token_issuer"],
    database=database,
    token_hasher=token_hasher
  )
  return {
    "authenticator": authenticator,
    "config_parser": config_parser,
    "cpu": cpu,
    "database": database,
    "disk": disk,
    "environment": environment,
    "logger": logger,
    "memory": memory,
    "password_hasher": password_hasher,
    "password_verifier": password_verifier,
    "token_hasher": token_hasher,
    "token_issuer": token_issuer
  }

def _build_repos_dict(database: Database) -> Dict[str, Any]:
  account_repository = AccountRepository(
    database=database
  )
  game_summary_repository = GameSummaryRepository(
    database=database
  )
  user_repository = UserRepository(
    database=database
  )
  return {
    "account": account_repository,
    "game_summary": game_summary_repository,
    "user": user_repository
  }

def _build_vars_dict(environment: Environment) -> Dict[str, Any]:
  users_admin_secret = environment.get_env_var(EnvVar.USERS_ADMIN_SECRET.value)
  return {
    "users_admin_secret": users_admin_secret
  }

#################### Config Builders ####################
def _build_cpu_config(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger:LoggerInterface
) -> CpuConfig:
  cpu_config_path = f"{config_dir}/{ConfigFilenames.CPU.value}"
  cpu_config_dict = disk.read_yaml(cpu_config_path)
  assert isinstance(cpu_config_dict, dict)
  return build_final_cpu_config(
    config_parser=config_parser,
    logger=logger,
    cpu_config_dict=cpu_config_dict
  )

def _build_database_config(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger: LoggerInterface
) -> DatabaseConfig:
  database_config_path = f"{config_dir}/{ConfigFilenames.DATABASE.value}"
  database_config_dict = disk.read_yaml(database_config_path)
  assert isinstance(database_config_dict, dict)
  return build_final_database_config(
    config_parser=config_parser,
    logger=logger,
    database_config_dict=database_config_dict
  )

def _build_disk_config(
  config_dir: str,
  config_parser: ConfigParser,
  temp_disk: Disk,
  logger: LoggerInterface
) -> DiskConfig:
  disk_config_path = f"{config_dir}/{ConfigFilenames.DISK.value}"
  disk_config_dict = temp_disk.read_yaml(disk_config_path)
  assert isinstance(disk_config_dict, dict)
  return build_final_disk_config(
    config_parser=config_parser,
    logger=logger,
    disk_config_dict=disk_config_dict,
  )

def _build_external_services_config(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger: LoggerInterface
) -> ExternalServicesConfig:
  external_service_config_path = f"{config_dir}/{ConfigFilenames.EXTERNAL_SERVICES.value}"
  external_services_config_dict = disk.read_yaml(external_service_config_path)
  assert isinstance(external_services_config_dict, dict)
  return build_final_external_services_config(
    config_parser=config_parser,
    logger=logger,
    external_services_config_dict=external_services_config_dict
  )

def _build_logger_config(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  temp_logger: LoggerInterface | None
) -> LoggerConfig:
  logger_config_path = f"{config_dir}/{ConfigFilenames.LOGGER.value}"
  logger_config_dict = disk.read_yaml(logger_config_path)
  assert isinstance(logger_config_dict, dict)
  return build_final_logger_config(
    config_parser=config_parser,
    logger=temp_logger,
    logger_config_dict=logger_config_dict
  )

def _build_memory_config(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger: LoggerInterface
) -> MemoryConfig:
  memory_config_path = f"{config_dir}/{ConfigFilenames.MEMORY.value}"
  memory_config_dict = disk.read_yaml(memory_config_path)
  assert isinstance(memory_config_dict, dict)
  return build_final_memory_config(
    config_parser=config_parser,
    logger=logger,
    memory_config_dict=memory_config_dict
  )

def _build_token_hasher_config(
  config_parser: ConfigParser,
  logger: LoggerInterface
) -> TokenHasherConfig:
  return build_final_token_hasher_config(
    config_parser=config_parser,
    logger=logger
  )

def _build_token_issuer_config(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger: LoggerInterface
) -> TokenIssuerConfig:
  token_issuer_config_path = f"{config_dir}/{ConfigFilenames.TOKEN_ISSUER.value}"
  token_issuer_config_dict = disk.read_yaml(token_issuer_config_path)
  assert isinstance(token_issuer_config_dict, dict)
  return build_final_token_issuer_config(
    config_parser=config_parser,
    logger=logger,
    token_issuer_config_dict=token_issuer_config_dict
  )

def _build_uvicorn_config(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger: LoggerInterface
) -> UvicornConfig:
  uvicorn_config_path = f"{config_dir}/{ConfigFilenames.UVICORN.value}"
  uvicorn_config_dict = disk.read_yaml(uvicorn_config_path)
  assert isinstance(uvicorn_config_dict, dict)
  return build_final_uvicorn_config(
    config_parser=config_parser,
    logger=logger,
    uvicorn_config_dict=uvicorn_config_dict
  )

#################### Infra Builders ####################

def _build_temp_disk(config_dir: str, config_parser: ConfigParser) -> Disk:
  disk_config_path = f"{config_dir}/{ConfigFilenames.DISK.value}"
  with open(disk_config_path, "r", encoding='utf-8') as yaml_file:
    raw_disk_config = yaml.safe_load(yaml_file)
    disk_config = config_parser.parse_disk_config(raw_disk_config)
    return Disk(disk_config)

def _build_authenticator(
  database: Database,
  token_hasher: TokenHasher
) -> Authenticator:
  return Authenticator(
    database=database,
    token_hasher=token_hasher
  )

def _build_cpu(cpu_config: CpuConfig) -> Cpu:
  return Cpu(
    cpu_config=cpu_config
  )

def _build_database(
  database_config: DatabaseConfig,
  logger: LoggerInterface
) -> Database:
  def _interruptible_sleep(seconds: float) -> None:
    end = time.time() + seconds
    try:
      while time.time() < end:
        time.sleep(0.1)
    except KeyboardInterrupt as e:
      raise e
  TIMEOUT = 3600.0
  RETRY_TIME = 5.0
  last_err = Exception()
  start_time = time.time()
  while time.time() - start_time < TIMEOUT:
    try:
      db = Database(database_config)
      return db
    except DatabaseInitializationErr as e:
      last_err = e
      logger.debug("Failed to connect to database. Trying again...")
      _interruptible_sleep(RETRY_TIME)
  if time.time() - start_time >= TIMEOUT:
    logger.critical("Timed our waiting for database initialization", error=last_err)
  raise TimeoutError("Timed out trying to connect to database.")

def _build_disk(disk_config: DiskConfig) -> Disk:
  return Disk(
    disk_config=disk_config
  )

def _build_logger(
  logger_config: LoggerConfig
) -> LoggerInterface:
  return SC2DataManagerLogger(
    logger_config=logger_config
  )

def _build_memory(memory_config: MemoryConfig) -> Memory:
  return Memory(
    memory_config=memory_config
  )

def _build_password_hasher() -> PasswordHasher:
  return PasswordHasher()

def _build_password_verifier() -> PasswordVerifier:
  return PasswordVerifier()

def _build_token_hasher(token_hasher_config: TokenHasherConfig) -> TokenHasher:
  return TokenHasher(
    token_hasher_config=token_hasher_config
  )

def _build_token_issuer(
  token_issuer_config: TokenIssuerConfig,
  database: Database,
  token_hasher: TokenHasher
) -> TokenIssuer:
  return TokenIssuer(
    token_issuer_config=token_issuer_config,
    database=database,
    token_hasher=token_hasher
  )
