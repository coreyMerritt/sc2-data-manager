#!/usr/bin/env bash
set -e
set -u
set -E
set -o pipefail
set -x

# Enforce early sudo so the script doesn't halt mid-execution
starting_user="$(id -un)"
starting_group="$(id -gn)"
sudo -k && sudo true

# Vars
cli_entrypoint_path="./src/composition/cli_entrypoint.py"
config_filenames_path="./src/composition/enums/config_filenames.py"
deployment_environment="$1"
[[ "$deployment_environment" == "test" ]] || [[ "$deployment_environment" == "dev" ]] || [[ "$deployment_environment" == "prod" ]] || {
  echo -e "\n\targ1 must be test|dev|prod\n"
  exit 1
}

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

# Package check
if ! jq --version 1>/dev/null; then
  echo -e "\n\tPackage needed: jq\n"
  exit 1
fi
sudo dnf install -y postgresql-libs postgresql-devel || sudo apt install -y libpq5 libpq-dev || true

# venv
if [[ ! -d ".venv" ]]; then
  python3 -m venv ".venv"
fi
source .venv/bin/activate

# Ensure dependencies are installed
pip install --upgrade pip setuptools wheel
if [[ "$deployment_environment" == "dev" ]]; then
  pip install -e .[infra,dev]
elif [[ "$deployment_environment" == "test" ]]; then
  pip install -e .[infra,dev]
elif [[ "$deployment_environment" == "prod" ]]; then
  pip install .[infra]
fi

# Dot env
if [[ ! -f "./.env" ]]; then
  cp -r "./.env.model" "./.env"
fi
sudo chmod 0644 "./.env"
sudo chown "$starting_user:$starting_group" "./.env"

# Set deployment to prod to get some basic vars for installation
[[ -f "./.env" ]] && source "./.env" || echo -e "\n\tWARNING: Proceeding without any .env file...\n"

# Config files
[[ -n "$SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR" ]]
[[ -n "$SC2_DATA_MANAGER_MODEL_CONFIG_DIR" ]]
config_filenames="$(cat "$config_filenames_path" | grep -v "import" | grep -v "class" | awk '{print $3}' | jq -r)"
## Assert all local config models exist
for config_filename in $config_filenames; do
  local_model_path="${SC2_DATA_MANAGER_MODEL_CONFIG_DIR}/${config_filename}"
  [[ -f "$local_model_path" ]] || {
    echo -e "\n\tFatal error: $local_model_path does not exist"
    exit 1
  }
done
## Ensure global config dir exists and has reasonable permissions
[[ -d "$SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR" ]] || {
  sudo mkdir "$SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR"
  sudo chown "$starting_user:$starting_group" "$SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR"
}
## Copy any missing global configs to their respective global dir
for config_filename in $config_filenames; do
  local_model_path="${SC2_DATA_MANAGER_MODEL_CONFIG_DIR}/${config_filename}"
  global_config_path="${SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR}/${config_filename}"
  [[ -f "$global_config_path" ]] || {
    sudo cp -r "$local_model_path" "$global_config_path"
  }
done
sudo chown -R "$starting_user:$starting_group" "$SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR"
sudo find "$SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR" -type f -exec chmod 644 {} +

# If is prod install, make binary and toss into /usr/bin
project_name_as_bin="sc2-data-manager"
installation_dir="/usr/bin"
installation_path="${installation_dir}/${project_name_as_bin}"
if [[ "$deployment_environment" == "prod" ]]; then
  ./.venv/bin/pyinstaller \
    --onefile \
    --hidden-import=composition.webserver.hook \
    --name=${project_name_as_bin} \
    "$cli_entrypoint_path"
  sudo cp "./dist/${project_name_as_bin}" "$installation_path"
  sudo chmod 755 "$installation_path"
fi
exit 0
