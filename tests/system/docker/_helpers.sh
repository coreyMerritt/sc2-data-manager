#!/usr/bin/env bash

function softCleanup() {
  # Remove loose container
  if docker ps | grep "$instance_name"; then
    docker stop "$instance_name"
  fi
  if docker ps -a | grep "$instance_name"; then
    docker rm "$instance_name"
  fi
  # Remove compose containers
  DOCKER_TAG="silences-a-silly-warning" docker compose --file "./docker/docker-compose.yml" down || true
  DOCKER_TAG="silences-a-silly-warning" docker compose down || true
}

function fullCleanup() {
  source ./.env
  project_name="$SC2_DATA_MANAGER_PROJECT_NAME"
  docker_image_tag="$1"
  instance_name="${project_name}_${docker_image_tag}"
  volume_name="$instance_name"
  # Remove loose container
  if docker ps | grep "$instance_name"; then
    docker stop "$instance_name"
  fi
  if docker ps -a | grep "$instance_name"; then
    docker rm "$instance_name"
  fi
  # Remove compose containers
  DOCKER_TAG="silences-a-silly-warning" docker compose --file "./docker/docker-compose.yml" down || true
  DOCKER_TAG="silences-a-silly-warning" docker compose down || true
  # Remove persistant items
  if docker images --format "{{.Repository}}:{{.Tag}}" | grep "$project_name" | grep "$docker_image_tag"; then
    docker rmi "${project_name}:${docker_image_tag}"
  fi
  if docker volume list | grep "$volume_name"; then
    docker volume rm "$volume_name"
  fi
}
