#!/usr/bin/env bash

set -o pipefail
set -u
set -x

function doesNotImport() {
  layer="$1"    # ex) infrastructure
  import="$2"   # ex) domain
  exception="${3-}"   # ex) mapper
  if [[ -n "$exception" ]]; then
    echo -e "\n\n\n\t========== $layer may not import from $import, UNLESS they are ${exception}s ==========\n"
    grep --color -rn " ${import}\." "src/${layer}/" --exclude-dir="__pycache__" \
      | awk "!(/\/${exception}s\// && /${exception}\.py/)" \
      | grep --color=always -E "src/${layer}|${import}\." \
      && exit 1
  else
    echo -e "\n\n\n\t========== $layer may not import from $import ==========\n"
    grep --color -rn " ${import}\." "src/${layer}/" --exclude-dir="__pycache__" \
      | grep --color=always -E "src/${layer}|${import}\." \
      && exit 1
  fi
}

# Tests
doesNotImport "interfaces/rest/health/controllers" "infrastructure"
doesNotImport "interfaces/rest/health/dtos" "infrastructure"
doesNotImport "interfaces/rest/health/routes" "infrastructure"
doesNotImport "interfaces/rest/v1/controllers" "infrastructure"
doesNotImport "interfaces/rest/v1/dtos" "infrastructure"
doesNotImport "interfaces/rest/v1/routes" "infrastructure"
doesNotImport "services" "interfaces"
doesNotImport "infrastructure" "services"
doesNotImport "infrastructure" "interfaces"
doesNotImport "domain" "infrastructure"
doesNotImport "domain" "services"
doesNotImport "domain" "interfaces"

exit 0
