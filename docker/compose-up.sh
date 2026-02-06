#!/usr/bin/env bash
set -e
set -E
set -o pipefail
set -u
set -x

# Args
set +u
docker_image_tag="test_pipelines" && [[ -n "$1" ]] && docker_image_tag="$1"
set -u

# Vars
source "./.env"
export POSTGRES_DB
export POSTGRES_USER
export COMPOSE_SC2_DATA_MANAGER
project_name="$SC2_DATA_MANAGER_PROJECT_NAME"
docker_compose_path="./docker/docker-compose.yml"

# Functions
function safeSed() {
  to_replace="$1"
  replacement="$2"
  tmp=$(mktemp)
  sed "s/$to_replace/$replacement/g" "./.env" > "$tmp"
  cat "$tmp" > "./.env"   # writes through the symlink, a direct write would break symlinks
  rm "$tmp"
}


# Ensure we're in the project root
while true; do
  if [[ -f "$(pwd)/pyproject.toml" ]]; then
    break
  elif [[ "$(pwd)" == "/" ]]; then
    set +x
    echo -e "\n\tFailed to find project root.\n"
    exit 1
  else
    cd ..
  fi
done

# Package Check
if ! which yq; then
  set +x
  echo -e "\n\Install yq and run again.\n"
  exit 1
fi

# Ensure everything is down before we starting messing with things
DOCKER_TAG="silences-a-silly-warning" docker compose --file "./docker/docker-compose.yml" down || true
DOCKER_TAG="silences-a-silly-warning" docker compose down || true

is_password="$(cat "./.env" | grep -oE "SC2_DATA_MANAGER_DATABASE_PASSWORD=.+")"
if [[ ! -n "$is_password" ]]; then
  new_password="$(openssl rand -hex 32)"
  POSTGRES_PASSWORD="$new_password"
  SC2_DATA_MANAGER_DATABASE_PASSWORD="$new_password"
  # Replace SC2_DATA_MANAGER_DATABASE_PASSWORD
  to_replace="$(cat "./.env" | grep -E "[.+]?SC2_DATA_MANAGER_DATABASE_PASSWORD.+")"
  replacement="SC2_DATA_MANAGER_DATABASE_PASSWORD=${new_password}"
  safeSed "$to_replace" "$replacement" "./.env"
  # Replace POSTGRES_PASSWORD
  to_replace="$(cat "./.env" | grep -E "[.+]?POSTGRES_PASSWORD.+")"
  replacement="POSTGRES_PASSWORD=${new_password}"
  safeSed "$to_replace" "$replacement" "./.env"
fi
# Ensure we're not trying to remount a used volume
docker_compose_path="./docker/docker-compose.yml"
volume_yq_paths=(
  ".volumes.postgres-18-volume.name"
  ".volumes.${project_name}-configs-volume.name"
)
for volume_yq_path in ${volume_yq_paths[@]}; do
  volume_name="$(cat "$docker_compose_path" | yq "$volume_yq_path")"
  if docker volume list | grep -o "$volume_name"; then
    set +x
    echo -e "\n\tVolume already exists: $volume_name"
    echo -e "\tIf credentials issues exist, consider removing the volume with:"
    echo -e "\t\tdocker volume rm $volume_name"
    set -x
  fi
done

# Do the thing
docker_image_tag="$docker_image_tag" docker compose \
  --env-file "$(cd "$(dirname "$0")/.." && pwd)/.env" \
  --file "$docker_compose_path" \
  up \
  --detach
