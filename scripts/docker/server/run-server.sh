#!/bin/bash
set -euox pipefail
IFS=$'\n\t'

set +u
source $(pipenv --venv)/bin/activate
set -u

CONFIG_PATH=/etc/its/env.json

larson get-parameters \
    --parameter-store-path $PARAMETER_PATH \
    > $CONFIG_PATH

source larson_json_to_vars $CONFIG_PATH

uwsgi --ini /opt/its/its.ini
