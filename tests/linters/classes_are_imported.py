#!/usr/bin/env python3
from linters._helpers import assert_all_classes_are_imported, ensure_in_project_root, get_classes, get_source_paths


def classes_are_imported() -> bool:
  ensure_in_project_root()
  source_paths = get_source_paths(recursive=True, base_dir="./src/")
  classes = get_classes(source_paths)
  assert_all_classes_are_imported(classes, source_paths)
  print("0: All classes are imported.")
  return True


if __name__ == "__main__":
  classes_are_imported()
