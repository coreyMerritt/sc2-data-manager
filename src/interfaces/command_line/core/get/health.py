import json
from dataclasses import asdict

from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.cpu import Cpu
from infrastructure.database.database import Database
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.logger.enums.logger_level import LoggerLevel
from infrastructure.memory.memory import Memory
from infrastructure.types.logger_interface import LoggerInterface
from services.health_manager import HealthManager


def get_full_health_report(
  logger: LoggerInterface,
  config_parser: ConfigParser,
  cpu: Cpu,
  database: Database,
  disk: Disk,
  environment: Environment,
  memory: Memory
) -> None:
  logger.set_level(LoggerLevel.WARNING)
  logger.set_json(False)
  health_manager = HealthManager(
    logger=logger,
    config_parser=config_parser,
    cpu=cpu,
    database=database,
    disk=disk,
    environment=environment,
    memory=memory
  )
  health_report_som = health_manager.get_full_health_report()
  print(json.dumps(asdict(health_report_som), indent=2))
