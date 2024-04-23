.ONESHELL:
ENV_PREFIX=$(shell python3 -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: build
build:          ## Install the project in dev mode.
	catkin build

.PHONY: test
test: coverage    ## Run tests and generate coverage report.
	$(ENV_PREFIX)coverage run --source='.' src/ros_snapd scripts/ -m pytest
	$(ENV_PREFIX)coverage report -m
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

.PHONY: test-black
test-black:
	$(ENV_PREFIX)black --check --diff src/ scripts/ setup.py

.PHONY: test-codespell
test-codespell:
	$(ENV_PREFIX)codespell src scripts setup.py

.PHONY: test-flake8
test-flake8:
	$(ENV_PREFIX)flake8 .

.PHONY: test-isort
test-isort:
	$(ENV_PREFIX)isort --diff --check src scripts setup.py

.PHONY: test-units
test-units: ## Run unit tests.
	$(ENV_PREFIX)pytest tests/

.PHONY: lint
lint: test-black test-codespell test-flake8 test-isort ## Run all linting tests.

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
	@rm -rf *.snap
