#!/bin/bash
set -euox pipefail
IFS=$'\n\t'

pipenv run uwsgi \
    --ini /opt/its/its.ini
