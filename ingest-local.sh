#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -u
set -x

files="$(ls ~/summary_files)"

for file in $files; do
  ./cli ingest summary ~/summary_files/$file
done
