#!/usr/bin/env bash

set -e
set -E
set -u
set -o pipefail
set -x

./docker/compose-up.sh "test_pipelines"

exit 0
