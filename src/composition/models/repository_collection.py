from dataclasses import dataclass

from domain.interfaces.repositories.user_repository_interface import UserRepositoryInterface


@dataclass
class RepositoryCollection:
  user: UserRepositoryInterface
