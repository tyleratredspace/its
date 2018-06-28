#!/usr/bin/env bash
set -euox pipefail
IFS=$'\n\t'

pipenv run mypy --config-file .mypy.ini its/loaders/file_system.py
