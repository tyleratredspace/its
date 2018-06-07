#!/bin/bash
set -euox pipefail
IFS=$'\n\t'

# TODO: use larson to load configuration from parameter store

pipenv run uwsgi --ini /opt/its/its.ini
