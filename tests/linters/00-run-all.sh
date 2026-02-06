#!/usr/bin/env bash

set -e
set -u
set -E
set -o pipefail
set -x

# Ensure we're in the project root
while true; do
  if [[ -f "$(pwd)/pyproject.toml" ]]; then
    break
  elif [[ "$(pwd)" == "/" ]]; then
    echo -e "\n\tFailed to find project root.\n"; exit 1
  else
    cd ..
  fi
done

# Deploy venv if not already deployed
if [[ ! -d ".venv" ]]; then
  python3 -m venv ".venv"
fi

# Validate some packages
which ".venv/bin/python"
which ".venv/bin/isort"
which ".venv/bin/mypy"
which ".venv/bin/pylint"
which ".venv/bin/ruff"

# Test
bash "./tests/linters/imports-flow-in-correct-direction.sh"
PYTHONPATH=./tests/ .venv/bin/python "./tests/linters/abstract_classes_have_an_abstract_method.py"
PYTHONPATH=./tests/ .venv/bin/python "./tests/linters/classes_are_implemented.py"
PYTHONPATH=./tests/ .venv/bin/python "./tests/linters/classes_are_imported.py"
PYTHONPATH=./tests/ .venv/bin/python "./tests/linters/errs_dont_inherit_directly_from_exception.py"
PYTHONPATH=./tests/ .venv/bin/python "./tests/linters/methods_declare_return_type.py"
PYTHONPATH=./tests/ .venv/bin/python "./tests/linters/methods_have_low_param_count.py"
PYTHONPATH=./tests/ .venv/bin/python "./tests/linters/service_exceptions_are_imported_in_interfaces.py"
.venv/bin/isort --check-only "."
.venv/bin/mypy "."
.venv/bin/pylint "./scripts/"
.venv/bin/pylint "./src/"
.venv/bin/pylint "./tests/"
.venv/bin/ruff check "."
exit 0
