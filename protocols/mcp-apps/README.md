# MCP Apps

MCP Apps is an official extension of MCP that lets a server deliver an interactive user interface with a tool. The server declares HTML views as resources and links tools to them. When the host calls such a tool, it renders the view in a sandboxed iframe. The view talks to the host with MCP's own JSON-RPC messages over `postMessage`.

It grew out of MCP-UI, which is now an SDK for it.

| | |
| --- | --- |
| Layer | interface |
| Author | MCP-UI and the Model Context Protocol project |
| Steward | Agentic AI Foundation (Linux Foundation) |
| Version | 2026-01-26 (2026-01-26) |
| Status | active |
| Spec | <https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx> |
| Repository | <https://github.com/modelcontextprotocol/ext-apps> |
| Schema | <https://github.com/modelcontextprotocol/ext-apps/blob/main/src/spec.types.ts> |
| License | Apache-2.0 |

## Roles

- **Server.** An MCP server. It declares the views and the tools that use them.
- **Host.** The MCP host. It renders views and relays their requests.
- **View.** The HTML page in the iframe. It acts as an MCP client of the host.
- **Sandbox proxy.** On web hosts, an iframe on a different origin that holds the view.

## Transport

`postMessage` between the iframe and the host. The host relays to the MCP server over the server's own MCP transport.

## Messages

JSON-RPC 2.0. A view resource has a `ui://` URI and the MIME type `text/html;profile=mcp-app`. A tool points at its view with `_meta.ui.resourceUri`, and `_meta.ui.visibility` says whether the model, the view, or both can call it.

The view can use standard MCP requests through the host, such as `tools/call` and `resources/read`, and these:

- View to host: `ui/initialize`, `ui/open-link`, `ui/message`, `ui/request-display-mode`, `ui/update-model-context`.
- Host to view: `ui/notifications/tool-input-partial`, `ui/notifications/tool-input`, `ui/notifications/tool-result`, `ui/notifications/tool-cancelled`, `ui/notifications/host-context-changed`, `ui/resource-teardown`.
- `ui/notifications/size-changed` from view to host.

The host passes theme values to the view as CSS variables.

## Connection

1. The host lists the server's resources and tools, and sees which tools have views.
2. The host calls a tool that has a view and, at the same time, renders the view.
3. The view sends `ui/initialize`. The host answers with its context and capabilities. The view sends `ui/notifications/initialized`.
4. The host sends the tool's arguments, then its result.
5. The view works with the user, calls tools and sends messages through the host.
6. The host sends `ui/resource-teardown` before it removes the view.

## Discovery

Through MCP. Views appear in `resources/list`, and tools reference them in `tools/list`. The host declares support under the extension id `io.modelcontextprotocol/ui` in its client capabilities, with the MIME types it can render.

## Authentication

None of its own. The view reaches the server only through the host, which uses its existing MCP connection. The iframe sandbox is mandatory.

## Example

A view resource. Source: <https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx>

```json
{
  "uri": "ui://weather-server/dashboard-template",
  "name": "weather_dashboard",
  "description": "Interactive weather dashboard view",
  "mimeType": "text/html;profile=mcp-app"
}
```

## Versions

Named by date, like MCP. 2026-01-26 is stable. The SDK `@modelcontextprotocol/ext-apps` has its own release numbers.

## References

- Specification: <https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx>
- Repository: <https://github.com/modelcontextprotocol/ext-apps>
- API documentation: <https://apps.extensions.modelcontextprotocol.io/api/>
- MCP-UI: <https://github.com/MCP-UI-Org/mcp-ui>
