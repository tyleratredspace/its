#!/usr/bin/env bash
set -euox pipefail
IFS=$'\n\t'

pipenv run black --check .
pipenv run isort --check-only --recursive .
