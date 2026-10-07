# Targets for the build and the checks. Run "make help" for the list.
.PHONY: help build check test lint contrast docs all

help:
	@echo "make build     write theme.css from src/"
	@echo "make check     test that theme.css is up to date"
	@echo "make test      run the unit tests"
	@echo "make lint      run stylelint (needs npx)"
	@echo "make contrast  check the contrast and the contrast doc"
	@echo "make docs      write the documents that come from the source"
	@echo "make all       check, test, lint, contrast, and test the documents"

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
	python3 scripts/check_contrast.py --presets

docs:
	python3 scripts/make_docs.py --write
	python3 scripts/font_coverage.py --write

all: check test lint contrast
	python3 scripts/make_docs.py --check-doc
	python3 scripts/font_coverage.py --check-doc
