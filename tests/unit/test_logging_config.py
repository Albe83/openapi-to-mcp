from __future__ import annotations

import io
import json
import logging

from openapi_to_mcp.logging_config import configure_logging


def test_configure_logging_emits_single_line_json_records() -> None:
    stream = io.StringIO()
    root_logger = logging.getLogger()
    original_handlers = list(root_logger.handlers)
    original_level = root_logger.level

    try:
        configure_logging(log_level="info", service="openapi-to-mcp-test", stream=stream)
        logger = logging.getLogger("openapi_to_mcp.tests")
        logger.info(
            "bootstrap completed",
            extra={"event": "bootstrap_completed", "request_id": "req-123"},
        )
    finally:
        root_logger.handlers = original_handlers
        root_logger.setLevel(original_level)

    lines = [line for line in stream.getvalue().splitlines() if line.strip()]
    assert len(lines) == 1

    payload = json.loads(lines[0])
    assert payload["timestamp"]
    assert payload["level"] == "info"
    assert payload["message"] == "bootstrap completed"
    assert payload["service"] == "openapi-to-mcp-test"
    assert payload["event"] == "bootstrap_completed"
    assert payload["request_id"] == "req-123"
