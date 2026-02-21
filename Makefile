IMAGE_NAME ?= openapi-to-mcp
CONTAINERFILE_VARIANT ?= mount

.PHONY: run test lint format \
	container-build-prod container-build-dev container-build-test container-build-all \
	container-smoke-prod container-quality-test

run:
	python3.11 -m openapi_to_mcp.main

test:
	python3.11 -m pytest -q

lint:
	python3.11 -m ruff check src tests

format:
	python3.11 -m ruff check --fix src tests

container-build-prod:
	CONTAINERFILE_VARIANT=$(CONTAINERFILE_VARIANT) ./scripts/container-build.sh prod $(IMAGE_NAME):prod

container-build-dev:
	CONTAINERFILE_VARIANT=$(CONTAINERFILE_VARIANT) ./scripts/container-build.sh dev $(IMAGE_NAME):dev

container-build-test:
	CONTAINERFILE_VARIANT=$(CONTAINERFILE_VARIANT) ./scripts/container-build.sh test $(IMAGE_NAME):test

container-build-all: container-build-prod container-build-dev container-build-test

container-smoke-prod:
	./scripts/container-test.sh smoke $(IMAGE_NAME):prod

container-quality-test:
	./scripts/container-test.sh quality $(IMAGE_NAME):test
