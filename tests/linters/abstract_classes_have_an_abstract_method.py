#!/usr/bin/env python3
import re
from logging import debug
from typing import List

from linters._helpers import Class, ensure_in_project_root, get_abstract_classes, get_source_paths


def abstract_classes_have_abstract_methods() -> bool:
  ensure_in_project_root()
  source_paths = get_source_paths(
    recursive=True,
    base_dir="./src/"
  )
  abstract_classes = get_abstract_classes(source_paths)
  for abstract_class in abstract_classes:
    print(abstract_class.name)
  __assert_all_abstract_classes_have_abstract_methods(abstract_classes)
  print("0: All abstract classes have at least one abstract method.")
  return True

def __assert_all_abstract_classes_have_abstract_methods(abstract_classes: List[Class]):
  for class_ in abstract_classes:
    fail_message = f"Abstract class doesn't contain abstract method:\n\t{class_.name}\n\t{class_.path}"
    assert __has_abstract_method(class_), fail_message

def __has_abstract_method(class_: Class) -> bool:
  debug(f"Checking class: {class_.name}")
  with open(class_.path, "r", encoding="utf-8") as source_file:
    lines = source_file.readlines()
  for _, line in enumerate(lines):
    abstract_method_match = re.search(r"@abstractmethod", line)
    if abstract_method_match:
      return True
  return False

if __name__ == "__main__":
  abstract_classes_have_abstract_methods()
