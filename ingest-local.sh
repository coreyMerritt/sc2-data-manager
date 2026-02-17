#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -u
set -x


game_summary_files_dir="~/summary_files"


files="$(ls "$game_summary_files_dir")"
for filename in $files; do
  ./cli ingest summary "${game_summary_files_dir}/${filename}"
done
