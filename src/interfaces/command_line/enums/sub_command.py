from enum import Enum


class SubCommand(str, Enum):
  GET = "get"
  INGEST = "ingest"
  RUN = "run"
