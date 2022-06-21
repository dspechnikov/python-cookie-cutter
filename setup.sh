#!/usr/bin/env bash

TEMPLATE_REPO_URL="https://github.com/dspechnikov/python-cookie-cutter"
DEFAULT_PROJECT_NAME="python_template"

echo -n "Project name (${DEFAULT_PROJECT_NAME}): "
read -r project_name

PROJECT_NAME=${project_name:-$DEFAULT_PROJECT_NAME}

git clone $TEMPLATE_REPO_URL "$PROJECT_NAME"

cd "$PROJECT_NAME" || exit

PIPENV_VENV_IN_PROJECT=1 pipenv install -d

pre-commit install
