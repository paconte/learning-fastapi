## This file is a modification of
## https://github.com/rochacbruno/python-project-template/blob/main/Makefile
.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	@echo "Running using $(ENV_PREFIX)"
	python -V
	python -m site


.PHONY: fmt
fmt:              ## Format code using black & isort.
	isort app/
	isort tests/
	black -l 79 app/
	black -l 79 tests/


.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	flake8 app/
	flake8 tests/
	black -l 79 --check app/
	black -l 79 --check tests/
	mypy --ignore-missing-imports app/
	mypy --ignore-missing-imports tests/


.PHONY: test
test: lint        ## Run tests and generate coverage report.
	pytest -v --cov-config .coveragerc --cov=src -l --tb=short --maxfail=1 tests/
	coverage xml
	coverage html