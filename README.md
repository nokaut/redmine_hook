# redmine_hook

## Export variables to env:

*REDMINE_URL* - Redmine URL

*REDMINE_TOKEN* - Redmine Personal Token

> For Github, Gitlab:

*REPO_URL_SCHEMA* - default http

> For AWS codecommit:

*AWS_REGION* - default eu-west-1


## Setup

pip install pre-commit
pre-commit install --hook-type post-commi

## Build package
python setup.py check
python setup.py bdist_wheel


## Install package
python setup.py install


################

`.pre-commit-hooks.yaml` config:

```yaml
repos:
  - repo: git://github.com/nokaut/redmine_hook
    rev: v0.6
    hooks:
      - id: redmine-commit-msg
        stages:
          - commit-msg
        name: NKT redmine-commit-msg
        always_run: true
        args: [ ".git/COMMIT_EDITMSG" ]
```
