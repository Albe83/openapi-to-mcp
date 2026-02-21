# Class Diagram - Streamable Lifecycle Fix

- Parent issue: [#19](https://github.com/Albe83/openapi-to-mcp/issues/19)
- ADR: [docs/adr/0002-fix-streamable-native-lifespan.md](../adr/0002-fix-streamable-native-lifespan.md)
- Purpose: Show transport classes and lifecycle coordination for native streamable mode.

```mermaid
classDiagram
  class FastMcpAdapter {
    -_native: bool
    -_runtime: object
    -_streamable_app: object?
    +supports_streamable_http: bool
    +streamable_http_app() object
    +native_lifespan() async context
    +register_tools(tools)
  }

  class FastAPIApp {
    +lifespan() async context
    +mount('/mcp', app)
  }

  class StartupOrchestrator {
    +bootstrap() GenerationReport
  }

  class FastMCPRuntime {
    +streamable_http_app() Starlette
    +tool(name, description)
  }

  class StarletteStreamableApp {
    +router.lifespan_context(app)
  }

  FastAPIApp --> StartupOrchestrator : bootstrap first
  FastAPIApp --> FastMcpAdapter : mounts and enters native lifespan
  FastMcpAdapter --> FastMCPRuntime : configure streamable_http_path='/'
  FastMcpAdapter --> StarletteStreamableApp : cache and reuse
```
