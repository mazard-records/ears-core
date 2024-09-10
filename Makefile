SRC := ears
TESTS := tests

PYTEST_OPTS := --doctest-modules
# PYTEST_OPTS += "--junitxml=junit/test-results-3.12.xml"

isort:
	poetry run isort $(SRC) $(TESTS)

ruff:
	poetry run ruff format $(SRC) $(TESTS)
	poetry run ruff check --fix $(SRC) $(TESTS)

lint: isort ruff

qa:
	poetry run isort --check $(SRC) $(TESTS)
	poetry run ruff check $(SRC) $(TESTS)
	poetry run mypy --strict $(SRC) $(TESTS)
	poetry run pytest $(TESTS) $(PYTEST_OPTS)
