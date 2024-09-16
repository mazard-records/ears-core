lint-functions:
	$(POETRY) run ruff format $(FUNCTIONS)
	$(POETRY) run ruff check --fix $(FUNCTIONS)

lint-package:
	$(POETRY) run ruff format $(SRC) $(TESTS)
	$(POETRY) run ruff check --fix $(SRC) $(TESTS)

lint-terraform:
	$(TERRAFORM) fmt

lint-all: lint-function lint-package lint-terraform