from dataclasses import dataclass

from domain.interfaces.authenticator import AuthenticatorInterface
from infrastructure.auth.password_hasher import PasswordHasher
from infrastructure.auth.password_verifier import PasswordVerifier
from infrastructure.auth.token_hasher import TokenHasher
from infrastructure.auth.token_issuer import TokenIssuer
from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.cpu import Cpu
from infrastructure.database.database import Database
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.memory.memory import Memory
from infrastructure.types.logger_interface import LoggerInterface


@dataclass
class InfrastructureCollection:
  authenticator: AuthenticatorInterface
  config_parser: ConfigParser
  cpu: Cpu
  database: Database
  disk: Disk
  environment: Environment
  logger: LoggerInterface
  memory: Memory
  password_hasher: PasswordHasher
  password_verifier: PasswordVerifier
  token_hasher: TokenHasher
  token_issuer: TokenIssuer
