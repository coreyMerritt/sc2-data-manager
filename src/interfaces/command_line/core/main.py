import argparse
import sys
from typing import Callable

from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.cpu import Cpu
from infrastructure.database.database import Database
from infrastructure.database.repositories.account_repository import AccountRepository
from infrastructure.database.repositories.game_summary_repository import GameSummaryRepository
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.memory.memory import Memory
from infrastructure.types.logger_interface import LoggerInterface
from interfaces.command_line.core.get.health import get_full_health_report
from interfaces.command_line.core.ingest.game_summary import ingest_game_summary
from interfaces.command_line.enums.get_target import GetTarget
from interfaces.command_line.enums.ingest_target import IngestTarget
from interfaces.command_line.enums.run_target import RunTarget
from interfaces.command_line.enums.sub_command import SubCommand
from interfaces.command_line.exceptions.unknown_command_exception import UnknownCommandException
from interfaces.command_line.exceptions.unknown_run_target_exception import UnknownRunTargetException


def add_default_command() -> None:
  if len(sys.argv) == 1:
    sys.argv = [sys.argv[0], "run", "server"]

def build_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(prog="foo_project_name")
  subparsers = parser.add_subparsers(dest="command", required=True)
  get_parser = subparsers.add_parser(SubCommand.GET.value)
  get_subparsers = get_parser.add_subparsers(dest="target", required=True)
  get_subparsers.add_parser(GetTarget.HEALTH_REPORT.value)
  run_parser = subparsers.add_parser(SubCommand.RUN.value)
  run_subparsers = run_parser.add_subparsers(dest="target", required=True)
  ingest_parser = subparsers.add_parser(SubCommand.INGEST.value)
  ingest_subparsers = ingest_parser.add_subparsers(dest="target", required=True)
  summary_parser = ingest_subparsers.add_parser(
    IngestTarget.SUMMARY.value
  )
  summary_parser.add_argument(
    "s2gs_file_path"
  )
  server_parser = run_subparsers.add_parser(RunTarget.SERVER.value)
  server_parser.add_argument(
    "--host",
    default=None,
    help="Host address to bind to",
    required=False,
    type=str
  )
  server_parser.add_argument(
    "--port",
    default=None,
    help="Host port to bind to",
    required=False,
    type=int
  )
  args = parser.parse_args()
  return args

def handle_args_routing(
  args: argparse.Namespace,
  logger: LoggerInterface,
  account_repository: AccountRepository,
  config_parser: ConfigParser,
  cpu: Cpu,
  database: Database,
  disk: Disk,
  environment: Environment,
  game_summary_repository: GameSummaryRepository,
  memory: Memory,
  run_webserver: Callable[[str | None, int | None], None]
) -> None:
  if args.command.lower() == SubCommand.GET.value:
    if args.target.lower() == GetTarget.HEALTH_REPORT.value:
      get_full_health_report(
        logger=logger,
        config_parser=config_parser,
        cpu=cpu,
        database=database,
        disk=disk,
        environment=environment,
        memory=memory
      )
  elif args.command.lower() == SubCommand.RUN.value:
    if args.target.lower() == RunTarget.SERVER.value:
      run_webserver(args.host, args.port)
    else:
      raise UnknownRunTargetException()
  elif args.command.lower() == SubCommand.INGEST.value:
    if args.target.lower() == IngestTarget.SUMMARY.value:
      ingest_game_summary(
        file_path=args.s2gs_file_path,
        logger=logger,
        account_repository=account_repository,
        game_summary_repository=game_summary_repository
      )
  else:
    raise UnknownCommandException()
