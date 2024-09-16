FUNCTIONS := functions
SRC := ears
TESTS := tests

POETRY := poetry
TERRAFORM := terraform
TERRAFORM += --chdir=terraform

version:
	$(POETRY) version --short

include bin/bld-lint.mk"
include bin/bld-qa.mk"
include bin/bld-tests.mk"

all: lint-all tests-all