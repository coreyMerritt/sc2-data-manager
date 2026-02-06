#!/usr/bin/env bash
set -e
set -E
set -o pipefail
set -u
set -x

grep \
  --color \
  --recursive \
  --line-number \
  --ignore-case \
  --exclude "deploy_db.log" \
  --exclude-dir "*cache*" \
  --exclude-dir "*egg-info*" \
  --exclude-dir "backups" \
  --exclude-dir ".git" \
  --exclude-dir ".venv" \
  "sc2-data-manager" \
  "." \
  2>/dev/null

grep \
  --color \
  --recursive \
  --line-number \
  --ignore-case \
  --exclude "deploy_db.log" \
  --exclude-dir "*cache*" \
  --exclude-dir "*egg-info*" \
  --exclude-dir "backups" \
  --exclude-dir ".git" \
  --exclude-dir ".venv" \
  "sc2_data_manager" \
  "." \
  2>/dev/null

grep \
  --color \
  --recursive \
  --line-number \
  --ignore-case \
  --exclude "deploy_db.log" \
  --exclude-dir "*cache*" \
  --exclude-dir "*egg-info*" \
  --exclude-dir "backups" \
  --exclude-dir ".git" \
  --exclude-dir ".venv" \
  "project_name" \
  "." \
  2>/dev/null
