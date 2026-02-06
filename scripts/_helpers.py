import os
import secrets
import sys
import tomllib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from subprocess import CalledProcessError, run

import yaml
from docker import DockerClient
from docker.errors import NotFound
from dotenv import load_dotenv


# Classes
@dataclass
class PostgresInfo:
  config_path: str
  container_name: str
  db_name: str
  host_port: int
  image_version: str
  password: str
  username: str

class BashError(Exception):
  message: str


# Public Functions
def debug(message: str) -> None:
  print(f"[DEBUG] {message}")

def info(message: str) -> None:
  print(f" [INFO] {message}")

def warn(message: str) -> None:
  print(f" [WARN] {message}")

def error(message: str) -> None:
  print(f"[ERROR] {message}")

def critical(message: str) -> None:
  print(f"\n\t[CRITICAL] {message}\n")
  sys.exit(1)

def output_seperator() -> None:
  print("=" * 120)

def filesystem_log(log_message: str, log_path: str) -> None:
  with open(log_path, "a", encoding="utf-8") as log_file:
    log_file.write(f"[{get_now_formatted_str()}] {log_message}\n")

def bash(cmd_str: str) -> str:
  try:
    return run(
      args=cmd_str,
      capture_output=True,
      check=True,
      shell=True,
      text=True
    ).stdout
  except CalledProcessError as e:
    message = "Bash call failed with:\n"
    message += f"\tSTDOUT: {e.stdout}\n"
    message += f"\tSTDERR: {e.stderr}\n"
    raise BashError(message) from e

def backup_db() -> None:
  IMAGE_VERSION = "18"
  POSTGRES_INFO: PostgresInfo = get_existing_database_info(IMAGE_VERSION)
  BACKUP_DIR = "./backups/database"
  TIMESTAMP = get_now_formatted_fs_safe_str()
  BACKUP_NAME = f"{TIMESTAMP}__{POSTGRES_INFO.container_name}.sql"
  BACKUP_PATH = f"{BACKUP_DIR}/{BACKUP_NAME}"
  bash(
    f"docker exec \
      {POSTGRES_INFO.container_name} \
      pg_dump \
        -U {POSTGRES_INFO.username} \
        {POSTGRES_INFO.db_name} \
      > {BACKUP_PATH}"
  )
  print("Backed up:")
  print(f"\t Database: {POSTGRES_INFO.db_name} {POSTGRES_INFO.username}@127.0.0.1:{POSTGRES_INFO.host_port}")
  print(f"\tContainer: {POSTGRES_INFO.container_name}")
  print(f"\t     Path: {BACKUP_PATH}")
  print()

def get_project_name() -> str:
  pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
  with pyproject_path.open("rb") as f:
    data = tomllib.load(f)
  if "project" in data and "name" in data["project"]:
    return data["project"]["name"]
  if "tool" in data and "poetry" in data["tool"] and "name" in data["tool"]["poetry"]:
    return data["tool"]["poetry"]["name"]
  raise KeyError("Project name not found in pyproject.toml")

def get_project_root() -> Path:
  current = Path(__file__).resolve().parent
  for parent in [current, *current.parents]:
    if (parent / "pyproject.toml").exists():
      return parent
  raise FileNotFoundError("pyproject.toml not found")

def is_docker_container_running(container_name: str, client: DockerClient) -> bool:
  try:
    container = client.containers.get(container_name)
    return container.status == "running"
  except NotFound:
    return False

def generate_new_database_info() -> PostgresInfo:
  load_dotenv()
  project_name = get_project_name()
  global_config_dir = os.getenv("SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR")
  assert global_config_dir
  database_config_path = f"{global_config_dir}/database.yml"
  postgres_username = f"{project_name.lower()}-user"
  postgres_password = _generate_password(32)
  postgres_dbname = f"{project_name.lower()}"
  host_port = 5432
  image_version = "18"
  container_name = f"postgres-{image_version}-{project_name.lower()}"
  return PostgresInfo(
    config_path=database_config_path,
    container_name=container_name,
    db_name=postgres_dbname,
    host_port=host_port,
    image_version=image_version,
    password=postgres_password,
    username=postgres_username
  )

def get_existing_database_info(image_version: str) -> PostgresInfo:
  project_name = get_project_name()
  global_config_dir = os.getenv("SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR")
  assert global_config_dir
  database_config_path = f"{global_config_dir}/database.yml"
  with open(database_config_path, "r", encoding="utf-8") as database_yaml_file:
    raw_database_config_dict = yaml.safe_load(database_yaml_file)
  container_name = f"postgres-{image_version}-{project_name.lower()}"
  return PostgresInfo(
    config_path=database_config_path,
    container_name=container_name,
    db_name=raw_database_config_dict["name"],
    host_port=raw_database_config_dict["port"],
    image_version=image_version,
    password=raw_database_config_dict["password"],
    username=raw_database_config_dict["username"]
  )

def require_sudo() -> None:
  if os.geteuid() != 0:
    critical("Run with sudo.")

def get_now_formatted_fs_safe_str() -> str:
  now = datetime.now(tz=UTC)
  formatted = now.strftime("%Y-%m-%d_%H-%M-%S-") + f"{int(now.microsecond / 1000):03d}"
  return formatted

def get_now_formatted_str() -> str:
  now = datetime.now(tz=UTC)
  formatted = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond / 1000):03d}"
  return formatted

def docker_volume_exists(volume_name: str, client: DockerClient) -> bool:
  try:
    client.volumes.get(volume_name)
    return True
  except NotFound:
    return False

# Private Functions
def _generate_password(length: int) -> str:
  return secrets.token_urlsafe(length)
