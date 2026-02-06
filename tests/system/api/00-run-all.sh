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
source "./tests/system/api/_helpers.sh"

# venv
if [[ ! -d ".venv" ]]; then
  python3 -m venv ".venv"
fi
source ".venv/bin/activate"

# Ensure test resources exist
startServer

# Test
bash "./tests/system/api/health-check.sh"

# Cleanup
cleanup
exit 0
