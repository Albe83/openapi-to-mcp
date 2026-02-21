"""Application entrypoint."""

from __future__ import annotations

import uvicorn

from openapi_to_mcp.config import Settings
from openapi_to_mcp.transport.app import create_app


def main() -> None:
    settings = Settings.from_env()
    app = create_app(settings)
    uvicorn.run(app, host=settings.mcp_host, port=settings.mcp_port)


if __name__ == "__main__":
    main()
