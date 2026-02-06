#!/usr/bin/env python3
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from subprocess import CalledProcessError, run
from typing import List


# Classes
@dataclass
class Parameter:
  name: str
  type: str

@dataclass
class Method:
  name: str
  parameters: List[Parameter]
  return_type: str
  content: List[str]

@dataclass
class Class:
  name: str
  methods: List[Method]
  path: str
  filename: str
  filestem: str

@dataclass
class Module:
  path: str
  filename: str
  filestem: str

@dataclass
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

def ensure_in_project_root() -> None:
  project_root = get_project_root()
  os.chdir(project_root)

def get_project_root() -> Path:
  current = Path(__file__).resolve().parent
  for parent in [current, *current.parents]:
    if (parent / "pyproject.toml").exists():
      return parent
  raise FileNotFoundError("pyproject.toml not found")

def get_source_paths(
  recursive: bool,
  base_dir: str,
  layer: str | None = None
) -> List[str]:
  if base_dir[-1] == "/":
    base_dir = base_dir[:-1]
  if layer:
    base_dir = f"{base_dir}/{layer}"
  base_dir = f"{base_dir}/"
  maxdepth = "-maxdepth 1"
  if recursive:
    maxdepth = "-maxdepth 99"
  cmd_return = bash(
    f"find {base_dir} {maxdepth} -type f \
      | grep -v \"__pycache__\" \
      | grep -F \".py\" \
      | grep -v \"__init__\""
  )
  source_paths_list = cmd_return.split("\n")
  source_paths_list.remove("")
  return source_paths_list

def assert_all_classes_are_imported(classes: List[Class], source_paths: List[str]):
  for class_ in classes:
    debug(f"Checking class: {class_.name}")
    assert is_imported_from_some_path(class_, source_paths), f"Never Imported:\n\t{class_.name}\n\t{class_.path}"

def is_imported_from_some_path(class_: Class, source_paths: List[str]) -> bool:
  for source_path in source_paths:
    if is_imported_from_specific_path(class_, source_path):
      return True
  return False

def is_imported_from_specific_path(class_: Class, source_path: str) -> bool:
  with open(source_path, "r", encoding="utf-8") as source_file:
    lines = source_file.readlines()
  for line in lines:
    match = re.match(fr"^from\ .+\ import\ ({class_.name})(?:,|\s|$)", line)
    if match:
      return True
  return False

def get_error_classes(paths: List[str]) -> List[Class]:
  err_identifiers = [
    "err",
    "exc"
  ]
  return _get_some_classes(paths, err_identifiers)

def get_abstract_classes(paths: List[str]) -> List[Class]:
  abs_identifiers = [
    "abstract",
    "abc"
  ]
  return _get_some_classes(paths, abs_identifiers)

def get_classes(paths: List[str]) -> List[Class]:
  class_list: List[Class] = []
  for path in paths:
    try:
      class_name = get_class_name(path)
      class_methods = get_class_methods(path)
      class_path = path
      class_filename = get_filename(path)
      class_filestem = get_filestem(path)
      class_ = Class(
        name=class_name,
        methods=class_methods,
        path=class_path,
        filename=class_filename,
        filestem=class_filestem
      )
      class_list.append(class_)
    except ValueError:
      continue
  class_list.sort(key=lambda c: c.name)
  return class_list

def get_class_methods(path: str) -> List[Method]:
  with open(path, "r", encoding="utf-8") as class_file:
    raw_class_data_lines = class_file.readlines()
  method_lines_lists = _get_list_of_method_lines_lists(raw_class_data_lines)
  methods: List[Method] = []
  for method_lines_list in method_lines_lists:
    method = _build_method(method_lines_list)
    methods.append(method)
  return methods

def get_modules(paths: List[str]) -> List[Module]:
  modules_list = []
  for path in paths:
    try:
      get_class_name(path)
      continue
    except ValueError:
      module_path = path
      module_filename = get_filename(path)
      module_filestem = get_filestem(path)
      module = Module(
        path=module_path,
        filename=module_filename,
        filestem=module_filestem
      )
      modules_list.append(module)
  return modules_list

def get_class_name(path: str) -> str:
  match = None
  class_name = None
  with open(path, "r", encoding="utf-8") as class_file:
    lines = class_file.readlines()
  for line in lines:
    match = re.match(r"^class ([A-Z][a-zA-Z]+)[:(]", line)
    if match:
      break
  if match:
    class_name = match.group(1)
  if class_name:
    return class_name
  raise ValueError("No class found")

def get_filename(path: str) -> str:
  return os.path.basename(path)

def get_filestem(path: str) -> str:
  return Path(path).stem

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
    message = "Bash call failed with:"
    message += f"\tSTDOUT: {e.stdout}"
    message += f"\tSTDERR: {e.stderr}"
    raise BashError(message) from e

def _get_list_of_method_lines_lists(raw_class_data_lines: List[str]) -> List[List[str]]:
  found_class_definition = False
  found_first_method = False
  rolling_method_lines: List[List[str]] = []
  current_method_lines: List[str] = []
  for line in raw_class_data_lines:
    if _is_class_definition(line):
      if not found_class_definition:
        found_class_definition = True
        continue
      raise RuntimeError("Found a second class in file.")
    if _is_method_definition(line):
      if len(current_method_lines) > 0:
        rolling_method_lines.append(current_method_lines)
        current_method_lines = []
      current_method_lines.append(line)
      if not found_first_method:
        found_first_method = True
      continue
    if found_first_method:
      current_method_lines.append(line)
  if len(current_method_lines) > 0:
    rolling_method_lines.append(current_method_lines)
  return rolling_method_lines

def _is_class_definition(line: str) -> bool:
  return bool(re.match(r"^\s*class\s+\w+\s*(\(.*\))?:", line))

def _is_method_definition(line: str) -> bool:
  return bool(re.match(r"^\s*def\s+\w+\s*\(.*\)\s?-?>?\s?.*:", line))

def _get_method_name(line: str) -> str:
  assert _is_method_definition(line)
  match = re.match(r"^\s*def\s+(\w+)\s*\(.*\)\s*-?>?\s?.*:", line)
  if not match:
    raise RuntimeError("Method definition does not contain a method name???")
  return match.group(1)

def _get_method_return_type(line: str) -> str:
  assert _is_method_definition(line)
  match = re.match(r"^\s*def\s+\w+\s*\(.*\)\s?-?>?\s?(.*):", line)
  if not match:
    return "Undefined"
  if match.group(1) == "":
    return "Undefined"
  return match.group(1)

def _get_method_parameters(line: str) -> List[Parameter]:
  assert _is_method_definition(line)
  match = re.match(r"^\s*def\s+\w+\s*\((.*?)\)\s*-?>?.*:", line)
  if not match:
    raise RuntimeError("Method definition does not contain any parameters???")
  raw_parameters = match.group(1).strip().replace(" ", "").split(",")
  parameters: List[Parameter] = []
  for raw_parameter in raw_parameters:
    raw_parameter_split = raw_parameter.split(":")
    assert len(raw_parameter_split) >= 1
    assert len(raw_parameter_split) <= 2
    parameter_name = raw_parameter_split[0]
    parameter_type = "Undefined"
    if len(raw_parameter_split) == 2:
      parameter_type = raw_parameter_split[1]
    parameters.append(
      Parameter(
        name=parameter_name,
        type=parameter_type
      )
    )
  return parameters

def _build_method(method_lines_list: List[str]) -> Method:
  return Method(
    name=_get_method_name(method_lines_list[0]),
    parameters=_get_method_parameters(method_lines_list[0]),
    return_type=_get_method_return_type(method_lines_list[0]),
    content=method_lines_list[1:]
  )


def _get_some_classes(paths: List[str], loose_matching_name_identifiers: List[str]) -> List[Class]:
  classes = get_classes(paths)
  some_classes: List[Class] = []
  for class_ in classes:
    for identifier in loose_matching_name_identifiers:
      if identifier.lower() in class_.name.lower():
        some_classes.append(class_)
        break
      if identifier.lower() in class_.path.lower():
        some_classes.append(class_)
        break
  return some_classes
