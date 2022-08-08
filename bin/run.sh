#!/bin/bash -xe

PROJ_ROOT="$(dirname $(readlink -f "${BASH_SOURCE[0]}"))/.."

export PYTHONPATH="${PROJ_ROOT}/src:${PYTHONPATH}"

exec flask --app my_www --debug run --host 0.0.0.0 --port "${BIND_PORT:-5000}" "$@"