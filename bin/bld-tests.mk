PYTEST_OPTS := --doctest-modules
PYTEST_OPTS += --cov-report xml
PYTEST_OPTS += --cov=ears.core tests/

tests-unit:
	$(POETRY) run pytest $(TESTS) $(PYTEST_OPTS)

tests-integration:

tests-e2e:

tests-all: tests-unit tests-integration tests-e2e
