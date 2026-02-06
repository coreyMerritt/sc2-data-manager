#!/usr/bin/env bash
set -e
set -E
set -u
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

# Test
bash "./tests/linters/00-run-all.sh"
bash "./tests/unit/00-run-all.sh"
bash "./tests/system/00-run-all.sh"
exit 0
