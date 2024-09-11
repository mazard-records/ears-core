SRC := ears
TESTS := tests

PY_VERSION = "3.12"

MYPY_OPTS := --strict
MYPY_OPTS += --namespace-packages
MYPY_OPTS += --explicit-package-bases

PYTEST_OPTS := --doctest-modules
PYTEST_OPTS += "--junitxml=.junit/test-results-$(PY_VERSION).xml"

isort-check:
	poetry run isort --check $(SRC) $(TESTS)

isort-format:
	poetry run isort $(SRC) $(TESTS)

ruff-check:
	poetry run ruff check $(SRC) $(TESTS)

ruff-format:
	poetry run ruff format $(SRC) $(TESTS)
	poetry run ruff check --fix $(SRC) $(TESTS)

mypy-check:
	poetry run mypy $(MYPY_OPTS) $(SRC) $(TESTS)

unit-tests:
	poetry run pytest $(TESTS) $(PYTEST_OPTS)

lint: isort-format ruff-format
qa: isort-check ruff-check mypy-check unit-tests