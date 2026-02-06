#!/usr/bin/env python3
import re
from logging import debug
from typing import List

from linters._helpers import Class, ensure_in_project_root, get_error_classes, get_source_paths

EXCEPTION_LIST = [
  "SC2DataManagerException"
]

def errs_dont_inherit_directly_from_exception() -> bool:
  ensure_in_project_root()
  source_paths = get_source_paths(recursive=True, base_dir="./src/")
  error_classes = get_error_classes(source_paths)
  __assert_all_errors_dont_inherit_from_exception(error_classes)
  print("0: All errors do not inherit from Exception.")
  return True

def __assert_all_errors_dont_inherit_from_exception(error_classes: List[Class]):
  for error_class in error_classes:
    if error_class.name not in EXCEPTION_LIST:
      assert not __inherits_from_exception(error_class), f"""
  Inherits from Exception:
     Path: {error_class.path}
    Class: {error_class.name}
"""

def __inherits_from_exception(error_class: Class) -> bool:
  debug(f"Checking class: {error_class.name}")
  with open(error_class.path, "r", encoding="utf-8") as source_file:
    lines = source_file.readlines()
  for _, line in enumerate(lines):
    line_is_error_definition = re.match(fr"error {error_class.name}", line)
    if line_is_error_definition:
      inherits_from_exc = re.search(r"\(Exception\):", line)
      if inherits_from_exc:
        return True
  return False


if __name__ == "__main__":
  errs_dont_inherit_directly_from_exception()
