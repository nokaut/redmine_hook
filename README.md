# redmine_hook

## Export variables to env:

REDMINE_URL - Redmine URL
REDMINE_TOKEN - Redmine Personal Token

For Github, Gitlab:
REPO_URL_SCHEMA - default http

For AWS codecommit:
AWS_REGION - default eu-west-1

## setup

pip install pre-commit
pre-commit install --hook-type commit-msg

## Build package
python setup.py check
python setup.py bdist_wheel

## Install package
python setup.py install
