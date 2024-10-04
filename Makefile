.ONESHELL:
.DEFAULT_GOAL := help
SHELL := /bin/bash

APP_NAME := drain_swamp_snippet

define NORMALIZE_APP_NAME
try:
    from importlib import metadata
except ImportError:
    v = '$(APP_NAME)'.replace('_', "-").replace('.', "-")
    print(v)
else:
    print(metadata.metadata('$(APP_NAME)')['Name']))
endef

#virtual environment. If 0 issue warning
#Not activated:0
#activated: 1
ifeq ($(VIRTUAL_ENV),)
$(warning virtualenv not activated)
is_venv =
else
is_venv = 1
VENV_BIN := $(VIRTUAL_ENV)/bin
VENV_BIN_PYTHON := python3
PY_X_Y=$(shell $(VENV_BIN_PYTHON) -c 'import platform; t_ver = platform.python_version_tuple(); print(".".join(t_ver[:2]));')
endif

ifeq ($(is_venv),1)
  # Package name is hyphen delimited
  PACKAGE_NAME ?= $(shell $(VENV_BIN_PYTHON) -c "$(NORMALIZE_APP_NAME)")
  VENV_PACKAGES ?= $(shell $(VENV_BIN_PYTHON) -m pip list --disable-pip-version-check --no-python-version-warning --no-input | /bin/awk '{print $$1}')
  IS_PACKAGE ?= $(findstring $(1),$(VENV_PACKAGES))

  is_wheel ?= $(call IS_PACKAGE,wheel)
  is_piptools ?= $(call IS_PACKAGE,pip-tools)

  find_whl = $(shell [[ -z "$(3)" ]] && extention=".whl" || extention="$(3)"; [[ -z "$(2)" ]] && srcdir="dist" || srcdir="$(2)/dist"; [[ -z "$(1)" ]] && whl=$$(ls $$srcdir/$(APP_NAME)*.whl  --format="single-column") || whl=$$(ls $$srcdir/$(1)*.whl --format="single-column"); echo $${whl##*/})
endif

##@ Helpers

# https://www.thapaliya.com/en/writings/well-documented-makefiles/
.PHONY: help
help:					## (Default) Display this help -- Always up to date
	@awk -F ':.*##' '/^[^: ]+:.*##/{printf "  \033[1m%-20s\033[m %s\n",$$1,$$2} /^##@/{printf "\n%s\n",substr($$0,5)}' $(MAKEFILE_LIST)

##@ Build dependencies

.PHONY: upgrade doc_upgrade diff_upgrade _upgrade
PIP_COMPILE = $(VENV_BIN_PYTHON) -m piptools compile --allow-unsafe --resolver=backtracking

upgrade:				## Update the *.lock files with the latest packages satisfying *.in files.
	@$(MAKE) _upgrade COMPILE_OPTS="--upgrade"

upgrade-one:			## Update the *.lock files for one package. `make upgrade-one package=...`
	@test -n "$(package)" || { echo "\nUsage: make upgrade-one package=...\n"; exit 1; }
	$(MAKE) _upgrade COMPILE_OPTS="--upgrade-package $(package)"

_upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
_upgrade:
ifeq ($(is_venv),1)
	@if [[ "$(PY_X_Y)" == "3.9" ]]; then

	@pip install --quiet --disable-pip-version-check -r requirements/pip-tools.lock
	$(PIP_COMPILE) -o requirements/pip.lock requirements/pip.in
	$(PIP_COMPILE) -o requirements/pip-tools.lock requirements/pip-tools.in
	$(PIP_COMPILE) -o requirements/kit.lock requirements/kit.in
	$(PIP_COMPILE) --no-strip-extras -o requirements/mypy.lock requirements/mypy.in
	$(PIP_COMPILE) --no-strip-extras -o requirements/tox.lock requirements/tox.in

	$(PIP_COMPILE) --no-strip-extras -o requirements/manage.lock requirements/manage.in
	$(PIP_COMPILE) --no-strip-extras -o requirements/dev.lock requirements/dev.in

	fi
endif

diff_upgrade:			## Summarize the last `make upgrade`
	@# The sort flags sort by the package name first, then by the -/+, and
	@# sort by version numbers, so we get a summary with lines like this:
	@#      -bashlex==0.16
	@#      +bashlex==0.17
	@#      -build==0.9.0
	@#      +build==0.10.0
	@/bin/git diff -U0 | /bin/grep -v '^@' | /bin/grep == | /bin/sort -k1.2,1.99 -k1.1,1.1r -u -V

##@ Testing

#run all pre-commit checks
.PHONY: pre-commit
pre-commit:				## Run checks found in .pre-commit-config.yaml
	@pre-commit run --all-files

#--strict is on
.PHONY: mypy
mypy:					## Static type checker (in strict mode)
ifeq ($(is_venv),1)
	@$(VENV_BIN_PYTHON) -m mypy -p $(APP_NAME)
endif

#make [check=1] black
.PHONY: black
black: private check_text = $(if $(check),"--check", "--quiet")
black:					## Code style --> In src and tests dirs, Code formatting. Sensible defaults -- make [check=1] black
ifeq ($(is_venv),1)
	@$(VENV_BIN)/black $(check_text) src/
	$(VENV_BIN)/black $(check_text) tests/
endif

.PHONY: isort
isort:					## Code style --> sorts imports
ifeq ($(is_venv),1)
	@$(VENV_BIN)/isort src/
	$(VENV_BIN)/isort tests/
endif

.PHONY: flake
flake:					## Code style --> flake8 extreme style nitpikker
ifeq ($(is_venv),1)
	@$(VENV_BIN_PYTHON) -m flake8 src/
	$(VENV_BIN_PYTHON) -m flake8 tests/
endif

# --cov-report=xml
# Dependencies: pytest, pytest-cov, pytest-regressions
# make [v=1] coverage
# @$(VENV_BIN)/pytest --showlocals --cov=drain_swamp_snippet --cov-report=term-missing --cov-config=pyproject.toml $(verbose_text) tests
.PHONY: coverage
coverage: private verbose_text = $(if $(v),"--verbose")
coverage:				## Run tests, generate coverage reports -- make [v=1] coverage
ifeq ($(is_venv),1)
	-@$(VENV_BIN_PYTHON) -m coverage erase
	@$(VENV_BIN_PYTHON) -m coverage run --parallel -m pytest --showlocals tests
	$(VENV_BIN_PYTHON) -m coverage combine
	$(VENV_BIN_PYTHON) -m coverage report --fail-under=95
endif

##@ Kitting
REPO_OWNER := msftcangoblowm/drain-swamp-snippet
REPO := $(REPO_OWNER)/drain_swamp_snippet

.PHONY: relbranch
relbranch:				## Create the branch for releasing (see howto.txt)
	@git switch -c $(REPO_OWNER)/release-$$(date +%Y%m%d)

.PHONY: install
install: override usage := make [force=1]
install: override check_web := Install failed. Possible cause no web connection
install: private force_text = $(if $(force),"--force-reinstall")
install:				## Installs *as a package*, not *with the ui* -- make [force=1] [debug=1] install
ifeq ($(is_venv),1)
  ifeq ($(is_wheel), wheel)
	@if [[  "$$?" -eq 0 ]]; then

	whl=$(call find_whl,$(APP_NAME),,) #1: PYPI package name (hyphens). 2 folder/app name (APP_NAME;underscores). 3 file extension
	echo $(whl)
	$(VENV_BIN_PYTHON) -m pip install --disable-pip-version-check --no-color --log="/tmp/$(APP_NAME)_install_prod.log" $(force_text) "dist/$$whl"

	fi

  endif
endif

.PHONY: install-force
install-force: force := 1
install-force: install	## Force install even if exact same version
