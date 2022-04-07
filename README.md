# redmine_hook

## Export variables to env:

*REDMINE_URL* - Redmine URL

*REDMINE_TOKEN* - Redmine Personal Token

> For Github, Gitlab:

*REPO_URL_SCHEMA* - default http

> For AWS codecommit:

*AWS_REGION* - default eu-west-1


## Setup

```bash
pip install pre-commit
pre-commit install --hook-type post-commit
```


## Build package

```bash
python setup.py check
python setup.py bdist_wheel
```


## Install package

```bash
python setup.py install
```


################

`.pre-commit-hooks.yaml` config:

```yaml
repos:
  - repo: git://github.com/nokaut/redmine_hook
    rev: v0.9.6
    hooks:
      - id: redmine-commit-check
        name: NKT redmine-commit-check validator
        always_run: true
      - id: redmine-commit-msg
        stages:
          - post-commit
        name: NKT redmine-commit-msg
        always_run: true

```
