from enum import Enum


class ConfigFilenames(str, Enum):
  CPU = "cpu.yml"
  DATABASE = "database.yml"
  DISK = "disk.yml"
  EXTERNAL_SERVICES = "external_services.yml"
  LOGGER = "logger.yml"
  MEMORY = "memory.yml"
  TOKEN_ISSUER = "token_issuer.yml"
  UVICORN = "uvicorn.yml"
