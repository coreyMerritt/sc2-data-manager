#!/usr/bin/env bash
set -e
set -E
set -u
set -o pipefail
set -x

# Vars
source ./.env
deployment_environment="test"
project_name="$SC2_DATA_MANAGER_PROJECT_NAME"
docker_image_tag="test_pipelines"
instance_name="${project_name}_${docker_image_tag}"
volume_name="${project_name}_${docker_image_tag}"

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
source "./tests/system/docker/_helpers.sh"

# Ensure test resources exist
fullCleanup "$docker_image_tag"
set +u
if ! docker images --format "{{.Repository}}:{{.Tag}}" | grep "$project_name" | grep "$docker_image_tag"; then
  ./docker/build.sh "test" "$docker_image_tag"
fi
set -u

# Test
bash "./tests/system/docker/image-runs.sh"
softCleanup
bash "./tests/system/docker/docker-compose-runs.sh"

# Cleanup
fullCleanup "$docker_image_tag"
exit 0
