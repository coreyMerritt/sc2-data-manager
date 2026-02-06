#!/usr/bin/env python3
from linters._helpers import (assert_all_classes_are_imported, ensure_in_project_root, get_error_classes,
                              get_source_paths)

MAX_ACCEPTABLE_ARG_COUNT = 2

def service_exceptions_are_imported_in_interfaces() -> bool:
  ensure_in_project_root()
  service_exception_paths = get_source_paths(
    recursive=True,
    base_dir="./src/",
    layer="services/exceptions"
  )
  interface_paths = get_source_paths(
    recursive=True,
    base_dir="./src/",
    layer="interfaces"
  )
  service_error_classes = get_error_classes(service_exception_paths)
  for error in service_error_classes.copy():
    if "Base" in error.name and "base" in error.path:
      service_error_classes.remove(error)
  assert_all_classes_are_imported(service_error_classes, interface_paths)
  print("0: All service-level errors are imported by some interface-level class.")
  return True


if __name__ == "__main__":
  service_exceptions_are_imported_in_interfaces()
