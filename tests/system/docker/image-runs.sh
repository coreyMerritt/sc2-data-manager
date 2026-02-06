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

# Vars
source ./.env
project_name="$SC2_DATA_MANAGER_PROJECT_NAME"
docker_image_tag="test_pipelines"
instance_name="${project_name}_${docker_image_tag}"

# Test
./docker/run.sh "$docker_image_tag"
timeout=30
container_is_healthy=0
didnt_time_out=0
start_time=$(date +%s)
while (( $(date +%s) - start_time < timeout )); do
  if res="$(docker exec "$instance_name" curl --silent http://localhost:8000/api/health | jq)"; then
    healthy="$(echo "$res" | jq .data.healthy)"
    if [[ "$healthy" == "true" ]]; then
      didnt_time_out=1
      container_is_healthy=1
      break
    fi
  fi
  sleep 1
done
(( didnt_time_out ))
(( container_is_healthy ))

exit 0
