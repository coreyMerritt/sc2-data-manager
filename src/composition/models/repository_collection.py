from dataclasses import dataclass

from domain.interfaces.repositories.user_repository_interface import UserRepositoryInterface
from infrastructure.database.repositories.account_repository import AccountRepository
from infrastructure.database.repositories.game_summary_repository import GameSummaryRepository


@dataclass
class RepositoryCollection:
  account: AccountRepository
  game_summary: GameSummaryRepository
  user: UserRepositoryInterface
