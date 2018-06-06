#!/usr/bin/env bash
set -euox pipefail
IFS=$'\n\t'

pipenv run black .
pipenv run isort --recursive .
