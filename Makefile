
.DEFAULT_GOAL := all

isort:
	poetry run isort .

black:
	poetry run black .

flake8:
	poetry run flake8 .

mypy:
	poetry run mypy --install-types --non-interactive .

audit_dependencies:
	poetry export --without-hashes -f requirements.txt | poetry run safety check --full-report --stdin

bandit:
	poetry run bandit -r . -x ./tests,./test

test:
	poetry run pytest

lint: isort black flake8 mypy

audit: audit_dependencies bandit

tests: test

all: lint audit tests
