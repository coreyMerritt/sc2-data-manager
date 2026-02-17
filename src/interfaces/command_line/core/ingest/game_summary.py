from infrastructure.database.repositories.account_repository import AccountRepository
from infrastructure.database.repositories.game_summary_repository import GameSummaryRepository
from infrastructure.disk.disk import Disk
from infrastructure.types.logger_interface import LoggerInterface
from services.exceptions.already_exists_err import AlreadyExistsErr
from services.game_summary_manager import GameSummaryManager


def ingest_game_summary(
  file_path: str,
  disk: Disk,
  logger: LoggerInterface,
  account_repository: AccountRepository,
  game_summary_repository: GameSummaryRepository
) -> None:
  logger.set_json(False)
  game_summary_manager = GameSummaryManager(
    disk=disk,
    logger=logger,
    account_repository=account_repository,
    game_summary_repository=game_summary_repository
  )
  with open(file_path, "rb") as f:
    try:
      game_summary_manager.ingest_game_summary(f.read())
    except AlreadyExistsErr:
      logger.error("Item already exists -- skipping...", error=None)
