#!/usr/bin/env bash
set -euox pipefail
IFS=$'\n\t'

pipenv run isort --recursive .
pipenv run black .
