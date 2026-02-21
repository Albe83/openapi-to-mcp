# Sequence Diagram - Streamable Request with Native Lifespan

- Parent issue: [#19](https://github.com/Albe83/openapi-to-mcp/issues/19)
- ADR: [docs/adr/0002-fix-streamable-native-lifespan.md](../adr/0002-fix-streamable-native-lifespan.md)
- Purpose: Show startup and request flow after native streamable lifecycle fix with canonical `POST /mcp`.

```mermaid
sequenceDiagram
  participant Runtime as FastAPI Runtime
  participant App as create_app Lifespan
  participant Orchestrator as StartupOrchestrator
  participant Adapter as FastMcpAdapter
  participant NativeApp as FastMCP Streamable App
  participant Agent as MCP Client
  participant Invoker as HttpxInvokerAdapter
  participant REST as Target REST API

  Runtime->>App: startup
  App->>Orchestrator: bootstrap()
  Orchestrator->>Adapter: register_tools(tools)
  App->>Adapter: enter native_lifespan()
  Adapter->>NativeApp: router.lifespan_context(app)
  NativeApp-->>Adapter: session manager initialized

  Agent->>Runtime: POST /mcp (JSON-RPC)
  Runtime->>NativeApp: dispatch mounted streamable request
  NativeApp->>Invoker: invoke(binding, payload)
  Invoker->>REST: HTTP request
  REST-->>Invoker: HTTP response
  Invoker-->>NativeApp: tool result
  NativeApp-->>Agent: MCP response

  Runtime->>App: shutdown
  App->>Adapter: exit native_lifespan()
```
