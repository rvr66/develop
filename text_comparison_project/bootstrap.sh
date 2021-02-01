#!/bin/sh
echo "test"
export FLASK_APP=./text_comaprison/index.py
source $(pipenv --venv)/bin/activate
flask run --host 0.0.0.0
