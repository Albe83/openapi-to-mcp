from __future__ import annotations

from pathlib import Path

import pytest

from openapi_to_mcp.adapters.openapi_source import FileOpenApiSourceAdapter, UrlOpenApiSourceAdapter
from openapi_to_mcp.errors import SourceLoadError


def test_file_source_loads_yaml(tmp_path: Path) -> None:
    spec_file = tmp_path / "openapi.yaml"
    spec_file.write_text("openapi: 3.1.0\npaths: {}\n", encoding="utf-8")

    adapter = FileOpenApiSourceAdapter(str(spec_file))
    loaded = adapter.load_raw()

    assert loaded["openapi"] == "3.1.0"


def test_file_source_raises_for_missing_file() -> None:
    adapter = FileOpenApiSourceAdapter("/tmp/does-not-exist.yaml")
    with pytest.raises(SourceLoadError):
        adapter.load_raw()


def test_url_source_uses_fetcher() -> None:
    expected = {"openapi": "3.1.0", "paths": {}}

    def fake_fetcher(url: str):
        assert url == "https://example.com/openapi.yaml"
        return expected

    adapter = UrlOpenApiSourceAdapter("https://example.com/openapi.yaml", fetcher=fake_fetcher)
    loaded = adapter.load_raw()

    assert loaded == expected
