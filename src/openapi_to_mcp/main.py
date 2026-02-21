"""Application entrypoint."""

from __future__ import annotations

import logging

import uvicorn

from openapi_to_mcp.config import Settings
from openapi_to_mcp.logging_config import configure_logging
from openapi_to_mcp.transport.app import create_app


def main() -> None:
    settings = Settings.from_env()
    configure_logging(log_level=settings.log_level)
    logger = logging.getLogger(__name__)
    app = create_app(settings)
    logger.info(
        "starting_openapi_to_mcp_server",
        extra={
            "event": "server_start",
            "host": settings.mcp_host,
            "port": settings.mcp_port,
        },
    )
    uvicorn.run(
        app,
        host=settings.mcp_host,
        port=settings.mcp_port,
        log_config=None,
    )


if __name__ == "__main__":
    main()
