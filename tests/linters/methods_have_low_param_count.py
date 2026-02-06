#!/usr/bin/env python3
import re
from typing import List

from linters._helpers import Class, debug, ensure_in_project_root, get_classes, get_source_paths

MAX_ACCEPTABLE_METHOD_COUNT = 3

def methods_have_low_method_count() -> bool:
  ensure_in_project_root()
  source_paths = get_source_paths(
    recursive=False,
    base_dir="./src/",
    layer="interfaces/rest/health/controllers"
  )
  source_paths.extend(
    get_source_paths(
      recursive=False,
      base_dir="./src/",
      layer="interfaces/rest/health/routes"
    )
  )
  source_paths.extend(
    get_source_paths(
      recursive=False,
      base_dir="./src/",
      layer="interfaces/rest/v1/controllers"
    )
  )
  source_paths.extend(
    get_source_paths(
      recursive=False,
      base_dir="./src/",
      layer="interfaces/rest/v1/routes"
    )
  )
  source_paths.extend(
    get_source_paths(
      recursive=True,
      base_dir="./src/",
      layer="infrastructure"
    )
  )
  source_paths.extend(
    get_source_paths(
      recursive=False,
      base_dir="./src/",
      layer="services"
    )
  )
  classes = get_classes(source_paths)
  __assert_all_classes_contain_proper_method_count(classes)
  print("0: All methods contain proper param counts.")
  return True

def __assert_all_classes_contain_proper_method_count(classes: List[Class]):
  for class_ in classes:
    fail_msg = f"Class method contains too many methods:\n\t{class_.name}\n\t{class_.path}"
    assert __contains_healthy_method_count(class_), fail_msg

def __contains_healthy_method_count(class_: Class) -> bool:
  debug(f"Checking class: {class_.name}")
  with open(class_.path, "r", encoding="utf-8") as source_file:
    lines = source_file.readlines()
  for _, line in enumerate(lines):
    method_match = re.search(r"^\s*def\s+\w+\s*\(([^)]*)\)", line)
    if method_match:
      method_name_match = re.search(r"^\s*def\s(.+)\(", line)
      method_name = "Unknown Method"
      if method_name_match:
        method_name = method_name_match.group(1)
      raw_methods = method_match.group(1)
      method_parameters = [a.strip() for a in raw_methods.split(",") if a.strip()]
      parameter_count = len(method_parameters)
      if "*args" in method_parameters:
        parameter_count -= 1
      if "**kwargs" in method_parameters:
        parameter_count -= 1
      fail_msg = f"Class method contains too many methods:\n\t{method_name}\n\t{class_.name}\n\t{class_.path}"
      assert parameter_count <= MAX_ACCEPTABLE_METHOD_COUNT + 1, fail_msg
  return True


if __name__ == "__main__":
  methods_have_low_method_count()
