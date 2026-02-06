#!/usr/bin/env python3
import re
from logging import debug
from typing import List

from linters._helpers import Class, ensure_in_project_root, get_classes, get_source_paths


def classes_are_implemented() -> bool:
  ensure_in_project_root()
  source_paths = get_source_paths(recursive=True, base_dir="./src/")
  classes = get_classes(source_paths)
  __assert_all_classes_are_implemented(classes)
  print("0: All classes are implemented.")
  return True

def __assert_all_classes_are_implemented(classes: List[Class]):
  for class_ in classes:
    assert __is_implemented(class_), f"Never Implemented:\n\t{class_.name}\n\t{class_.path}"

def __is_implemented(class_: Class) -> bool:
  debug(f"Checking class: {class_.name}")
  with open(class_.path, "r", encoding="utf-8") as source_file:
    lines = source_file.readlines()
  for i, line in enumerate(lines):
    line_is_class_match = re.match(fr"^class {class_.name}", line)
    if line_is_class_match:
      line_contains_unimplemented = re.match(r"^\s*(pass|\.\.\.)\s*$", line)
      try:
        next_line_contains_unimplemented = re.match(r"^\s*(pass|\.\.\.)\s*$", lines[i+1])
      except IndexError:
        next_line_contains_unimplemented = None
      if line_contains_unimplemented or next_line_contains_unimplemented:
        return False
  return True


if __name__ == "__main__":
  classes_are_implemented()
