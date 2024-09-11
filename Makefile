SRC := ears
TESTS := tests

PY_VERSION = "3.12"

MYPY_OPTS := --strict
MYPY_OPTS += --namespace-packages
MYPY_OPTS += --explicit-package-bases

PYTEST_OPTS := --doctest-modules
PYTEST_OPTS += "--junitxml=.junit/test-results-$(PY_VERSION).xml"

ruff-check:
	poetry run ruff check $(SRC) $(TESTS)

mypy-check:
	poetry run mypy $(MYPY_OPTS) $(SRC) $(TESTS)

unit-tests:
	poetry run pytest $(TESTS) $(PYTEST_OPTS)

lint:
	poetry run ruff format $(SRC) $(TESTS)
	poetry run ruff check --fix $(SRC) $(TESTS)

qa: ruff-check mypy-check unit-tests