#!/usr/bin/env bash

set -e
set -E
set -u
set -o pipefail
set -x

timeout=5
start_time=$(date +%s)
current_time=$(date +%s)
health_check_hit="false"
health_check_healthy="false"
while (( current_time - start_time < timeout )); do
  response="$(curl --silent --location "http://127.0.0.1:8000/api/health" | jq)" || true
  healthy="$(echo "$response" | jq .data.healthy)" || true
  if [[ "$health_check_hit" == "false" && -n "$healthy" ]]; then
    health_check_hit="true"
  fi
  if [[ "$healthy" == "true" || "$healthy" == "True" ]]; then
    health_check_healthy="true"
    break
  fi
  sleep 1
  current_time=$(date +%s)
done
error="$(echo "$response" | jq -r .error)"
[[ "$health_check_hit" == "true" ]] || {
  echo -e "\n\tFailed to hit health endpoint"
  exit 1
}
[[ "$health_check_healthy" == "true" ]] || {
  echo -e "\n\tHealth endpoint did not return healthy"
  exit 1
}
[[ "$error" == "null" ]] || {
  echo -e "\n\t\"error\" is not null"
  exit 1
}

exit 0
