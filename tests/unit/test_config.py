from __future__ import annotations

import pytest

from openapi_to_mcp.config import Settings
from openapi_to_mcp.errors import ConfigurationError


def test_settings_requires_openapi_source() -> None:
    with pytest.raises(ConfigurationError):
        Settings.from_env({})


def test_settings_defaults_and_path_precedence() -> None:
    settings = Settings.from_env(
        {
            "OPENAPI_SPEC_PATH": "./spec.yaml",
            "OPENAPI_SPEC_URL": "https://example.com/openapi.yaml",
        }
    )

    assert settings.mcp_host == "0.0.0.0"
    assert settings.mcp_port == 8080
    assert settings.log_level == "info"
    assert settings.resolve_openapi_source() == ("path", "./spec.yaml")


def test_settings_invalid_port() -> None:
    with pytest.raises(ConfigurationError):
        Settings.from_env({"OPENAPI_SPEC_PATH": "./spec.yaml", "MCP_PORT": "abc"})


def test_settings_invalid_log_level() -> None:
    with pytest.raises(ConfigurationError):
        Settings.from_env({"OPENAPI_SPEC_PATH": "./spec.yaml", "LOG_LEVEL": "verbose"})
