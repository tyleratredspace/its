#!/bin/bash
set -euox pipefail
IFS=$'\n\t'

set +u
source $(pipenv --venv)/bin/activate
set -u

APP_CONFIG_PATH=/etc/its/env.json
UWSGI_CONFIG_PATH=/opt/its/its.ini

larson get-parameters \
    --parameter-store-path $PARAMETER_PATH \
    > $APP_CONFIG_PATH

source larson_json_to_vars $APP_CONFIG_PATH

if [ -z "$ITS_NEWRELIC_LICENSE" ]; then
    # no newrelic license key configured, run uwsgi plain
    exec uwsgi --ini $UWSGI_CONFIG_PATH
else
    # newrelic license key available, generate config file then
    # run uwsgi in newrelic wrapper
    confd -onetime -backend file -file $APP_CONFIG_PATH
    exec NEW_RELIC_CONFIG_FILE=/etc/its/newrelic.ini newrelic-admin run-program \
        uwsgi --ini $UWSGI_CONFIG_PATH
fi
