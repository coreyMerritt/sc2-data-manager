from dataclasses import dataclass


@dataclass(frozen=True)
class CreateGameSummarySOM:
  filehash: str
