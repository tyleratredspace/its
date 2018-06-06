#!/bin/bash
set -euox pipefail
IFS=$'\n\t'

FLASK_APP=its/application.py
FLASK_ENV=development

export FLASK_APP
export FLASK_ENV

pipenv run flask run
