from __future__ import annotations

from openapi_to_mcp.application.mapper import OperationMapper


def test_operation_mapper_maps_operations_and_parameters() -> None:
    spec = {
        "openapi": "3.1.0",
        "servers": [{"url": "https://api.example.com"}],
        "paths": {
            "/pets/{petId}": {
                "parameters": [
                    {
                        "name": "petId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "get": {
                    "operationId": "getPet",
                    "parameters": [
                        {
                            "name": "includeHistory",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "boolean"},
                        }
                    ],
                    "responses": {"200": {"description": "ok"}},
                },
            }
        },
    }

    operations = OperationMapper().map_operations(spec)

    assert len(operations) == 1
    op = operations[0]
    assert op.operation_id == "getPet"
    assert op.server_url == "https://api.example.com"
    names = {f"{p['in']}:{p['name']}" for p in op.parameters}
    assert names == {"path:petId", "query:includeHistory"}


def test_operation_mapper_uses_server_override_precedence() -> None:
    spec = {
        "openapi": "3.1.0",
        "servers": [{"url": "https://root.example.com"}],
        "paths": {
            "/root-only": {
                "get": {
                    "operationId": "rootOnly",
                    "responses": {"200": {"description": "ok"}},
                }
            },
            "/path-level": {
                "servers": [{"url": "https://path.example.com"}],
                "get": {
                    "operationId": "pathLevel",
                    "responses": {"200": {"description": "ok"}},
                },
            },
            "/operation-level": {
                "servers": [{"url": "https://path-override.example.com"}],
                "get": {
                    "operationId": "operationLevel",
                    "servers": [{"url": "https://operation.example.com"}],
                    "responses": {"200": {"description": "ok"}},
                },
            },
        },
    }

    operations = OperationMapper().map_operations(spec)
    by_id = {op.operation_id: op for op in operations}

    assert by_id["rootOnly"].server_url == "https://root.example.com"
    assert by_id["pathLevel"].server_url == "https://path.example.com"
    assert by_id["operationLevel"].server_url == "https://operation.example.com"
