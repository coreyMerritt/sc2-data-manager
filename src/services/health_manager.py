import json
from dataclasses import asdict

from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.cpu import Cpu
from infrastructure.database.database import Database
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.memory.memory import Memory
from infrastructure.types.logger_interface import LoggerInterface
from services.base_service import BaseService
from services.models.outputs.full_health_report_som import FullHealthReportSOM


class HealthManager(BaseService):
  _logger: LoggerInterface
  _config_parser: ConfigParser
  _cpu: Cpu
  _database: Database
  _disk: Disk
  _environment: Environment
  _memory: Memory

  def __init__(
    self,
    logger: LoggerInterface,
    config_parser: ConfigParser,
    cpu: Cpu,
    database: Database,
    disk: Disk,
    environment: Environment,
    memory: Memory
  ):
    self._config_parser = config_parser
    self._cpu = cpu
    self._database = database
    self._disk = disk
    self._environment = environment
    self._memory = memory
    super().__init__(logger)

  def get_full_health_report(self) -> FullHealthReportSOM:
    config_parser_health_report = self._config_parser.get_health_report()
    cpu_health_report = self._cpu.get_health_report()
    database_health_report = self._database.get_health_report()
    disk_health_report = self._disk.get_health_report()
    environment_health_report = self._environment.get_health_report()
    logger_health_report = self._logger.get_health_report()
    memory_health_report = self._memory.get_health_report()
    full_health_report = FullHealthReportSOM(
      config_parser_health_report=config_parser_health_report,
      cpu_health_report=cpu_health_report,
      database_health_report=database_health_report,
      disk_health_report=disk_health_report,
      environment_health_report=environment_health_report,
      logger_health_report=logger_health_report,
      memory_health_report=memory_health_report
    )
    self._logger.debug(f"System Health:\n{json.dumps(asdict(full_health_report), indent=2)}")
    return full_health_report
