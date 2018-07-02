#!/usr/bin/env bash
set -euox pipefail
IFS=$'\n\t'

pipenv run black --check .
pipenv run prospector --profile .prospector.yml .
