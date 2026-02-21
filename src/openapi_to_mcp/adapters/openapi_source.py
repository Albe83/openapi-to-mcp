"""OpenAPI source adapters for file and URL inputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, Optional

import httpx
import yaml

from openapi_to_mcp.errors import SourceLoadError


class FileOpenApiSourceAdapter:
    """Load an OpenAPI document from local filesystem."""

    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def load_raw(self) -> Dict[str, Any]:
        if not self._path.exists() or not self._path.is_file():
            raise SourceLoadError(f"OpenAPI file not found: {self._path}")

        try:
            raw_text = self._path.read_text(encoding="utf-8")
            loaded = yaml.safe_load(raw_text)
        except OSError as exc:
            raise SourceLoadError(f"Cannot read OpenAPI file: {self._path}") from exc
        except yaml.YAMLError as exc:
            raise SourceLoadError(f"Invalid YAML/JSON in OpenAPI file: {self._path}") from exc

        if not isinstance(loaded, dict):
            raise SourceLoadError("OpenAPI file content must be an object.")
        return loaded


class UrlOpenApiSourceAdapter:
    """Load an OpenAPI document from remote URL."""

    def __init__(
        self,
        url: str,
        timeout_seconds: float = 10.0,
        fetcher: Optional[Callable[[str], Dict[str, Any]]] = None,
    ) -> None:
        self._url = url
        self._timeout_seconds = timeout_seconds
        self._fetcher = fetcher

    def load_raw(self) -> Dict[str, Any]:
        if self._fetcher is not None:
            return self._fetcher(self._url)

        try:
            response = httpx.get(self._url, timeout=self._timeout_seconds)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise SourceLoadError(f"Cannot fetch OpenAPI URL: {self._url}") from exc

        try:
            loaded = yaml.safe_load(response.text)
        except yaml.YAMLError as exc:
            raise SourceLoadError(f"Invalid YAML/JSON from URL: {self._url}") from exc

        if not isinstance(loaded, dict):
            raise SourceLoadError("OpenAPI URL content must be an object.")
        return loaded
