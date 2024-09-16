MYPY_OPTS := --strict
MYPY_OPTS += --namespace-packages
MYPY_OPTS += --explicit-package-bases

qa-functions:
	$(POETRY) run ruff check $(FUNCTIONS)
	$(POETRY) run mypy $(MYPY_OPTS) $(FUNCTIONS)

qa-package:
	$(POETRY) run ruff check $(SRC) $(TESTS)
	$(POETRY) run mypy $(MYPY_OPTS) $(SRC) $(TESTS)

qa-terraform:
	$(TERRAFORM) fmt -check
	$(TERRAFORM) validate

qa-all: qa-function qa-package qa-terraform
