#!/usr/bin/env python3
from logging import debug
from typing import List

from linters._helpers import Class, ensure_in_project_root, get_classes, get_source_paths

METHOD_NAME_EXCEPTION_LIST = [
  "__eq__",
  "__init__",
  "__post_init__"
]

def methods_declare_return_type() -> bool:
  ensure_in_project_root()
  source_paths = get_source_paths(
    recursive=True,
    base_dir="./src/"
  )
  classes = get_classes(source_paths)
  __assert_all_methods_declare_return_type(classes)
  print("0: All methods declare a return type.")
  return True

def __assert_all_methods_declare_return_type(classes: List[Class]) -> None:
  for class_ in classes:
    debug(f"Checking class: {class_.name}")
    for class_method in class_.methods:
      debug(f"Checking method: {class_method.name}")
      if class_method.name in METHOD_NAME_EXCEPTION_LIST:
        continue
      fail_msg = f"""
  Return type is not defined:
      Path: {class_.path}
     Class: {class_.name}
    Method: {class_method.name}
"""
      assert class_method.return_type != "Undefined", fail_msg


if __name__ == "__main__":
  methods_declare_return_type()
