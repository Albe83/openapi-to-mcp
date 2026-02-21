.PHONY: run test lint format

run:
	python3.11 -m openapi_to_mcp.main

test:
	python3.11 -m pytest -q

lint:
	python3.11 -m ruff check src tests

format:
	python3.11 -m ruff check --fix src tests
