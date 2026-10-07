# Targets for the build and the checks. Run "make help" for the list.
.PHONY: help build check test lint contrast all

help:
	@echo "make build     write theme.css from src/"
	@echo "make check     test that theme.css is up to date"
	@echo "make test      run the unit tests"
	@echo "make lint      run stylelint (needs npx)"
	@echo "make contrast  check the contrast and the contrast doc"
	@echo "make all       check, test, lint, and contrast"

build:
	./build.sh

check:
	./build.sh --check

test:
	python3 -m unittest discover -s tests

lint:
	npx --yes stylelint@16 "src/*.css" "snippets/*.css"

contrast:
	python3 scripts/check_contrast.py
	python3 scripts/check_contrast.py --check-doc

all: check test lint contrast
