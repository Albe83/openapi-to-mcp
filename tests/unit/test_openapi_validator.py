from __future__ import annotations

import pytest

from openapi_to_mcp.adapters.openapi_validator import OpenApiValidatorAdapter
from openapi_to_mcp.errors import OpenApiValidationError


def test_validator_accepts_minimal_valid_spec() -> None:
    validator = OpenApiValidatorAdapter()
    result = validator.validate(
        {
            "openapi": "3.1.0",
            "servers": [{"url": "https://api.example.com"}],
            "paths": {
                "/pets": {
                    "get": {
                        "operationId": "listPets",
                        "responses": {"200": {"description": "ok"}},
                    }
                }
            },
        }
    )

    assert result.spec["openapi"] == "3.1.0"
    assert result.warnings == []


def test_validator_warns_on_missing_operation_id() -> None:
    validator = OpenApiValidatorAdapter()
    result = validator.validate(
        {
            "openapi": "3.1.0",
            "servers": [{"url": "https://api.example.com"}],
            "paths": {"/pets": {"get": {"responses": {"200": {"description": "ok"}}}}},
        }
    )

    assert len(result.warnings) == 1


def test_validator_rejects_missing_paths() -> None:
    validator = OpenApiValidatorAdapter()
    with pytest.raises(OpenApiValidationError):
        validator.validate({"openapi": "3.1.0"})


def test_validator_rejects_operation_without_resolvable_server_url() -> None:
    validator = OpenApiValidatorAdapter()
    with pytest.raises(OpenApiValidationError):
        validator.validate(
            {
                "openapi": "3.1.0",
                "paths": {
                    "/pets": {
                        "get": {
                            "operationId": "listPets",
                            "responses": {"200": {"description": "ok"}},
                        }
                    }
                },
            }
        )


def test_validator_accepts_operation_level_server_override() -> None:
    validator = OpenApiValidatorAdapter()
    result = validator.validate(
        {
            "openapi": "3.1.0",
            "paths": {
                "/pets": {
                    "get": {
                        "operationId": "listPets",
                        "servers": [{"url": "https://op.example.com"}],
                        "responses": {"200": {"description": "ok"}},
                    }
                }
            },
        }
    )

    assert result.spec["openapi"] == "3.1.0"
