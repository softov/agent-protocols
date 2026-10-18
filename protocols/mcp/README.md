# Model Context Protocol (MCP)

MCP connects an AI application to servers that give it tools, data and prompts. One server can serve many applications, and one application can use many servers. Since version 2026-07-28 the protocol is stateless: there is no handshake and no session, and every request carries the protocol version and the client's capabilities.

| | |
| --- | --- |
| Layer | context |
| Author | Anthropic |
| Steward | Agentic AI Foundation (Linux Foundation) |
| Version | 2026-07-28 (2026-07-28) |
| Status | active |
| Spec | <https://modelcontextprotocol.io/specification/2026-07-28> |
| Repository | <https://github.com/modelcontextprotocol/modelcontextprotocol> |
| Schema | <https://github.com/modelcontextprotocol/modelcontextprotocol/tree/main/schema/2026-07-28> |
| License | Apache-2.0 |

## Roles

- **Host.** The AI application the user runs. It holds one client per server.
- **Client.** The connector inside the host that talks to one server.
- **Server.** A program that exposes tools, resources and prompts.

## Transport

- **stdio.** The client starts the server as a subprocess. Messages are newline-delimited JSON on stdin and stdout.
- **Streamable HTTP.** The client sends each message as an HTTP POST to one endpoint. The server answers with one JSON object or with a Server-Sent Events stream for that request. POST requests carry the `MCP-Protocol-Version`, `Mcp-Method` and `Mcp-Name` headers.

Custom transports are allowed. The older HTTP+SSE transport is deprecated.

## Messages

JSON-RPC 2.0 in UTF-8. Since 2026-07-28 only the client sends requests. Every result carries `resultType`: `complete`, or `input_required` when the server needs more input.

Server features:

- **Tools.** Functions the model can call. `tools/list`, `tools/call`.
- **Resources.** Data the client can read, by URI. `resources/list`, `resources/read`, `resources/templates/list`.
- **Prompts.** Message templates the user can pick. `prompts/list`, `prompts/get`.
- **Utilities.** Completion, logging, pagination, and cache hints (`ttlMs`, `cacheScope`) on list and read results.

Client features:

- **Elicitation.** The server asks the user for input.
- **Sampling.** The server asks the client's model for a completion. Deprecated.
- **Roots.** The client tells the server which directories it may use. Deprecated.

The server asks for these with a multi round-trip request: it returns `input_required` with `inputRequests`, and the client sends the original request again with `inputResponses`.

`subscriptions/listen` opens one long-lived stream for change notifications the client opts in to. Tasks and MCP Apps are official extensions, outside the core spec.

## Connection

There is no handshake.

1. The client may call `server/discover` to learn the server's versions, capabilities and identity. Every server must implement it.
2. Each request carries, in `_meta`, the protocol version, the client's capabilities and, as a recommendation, the client's identity.
3. Each result carries the server's identity in `_meta`.

State that must survive between calls is passed as explicit handles in tool arguments. A broken response stream loses its request, and the client sends it again with a new id.

Versions up to 2025-11-25 used an `initialize` request and an `Mcp-Session-Id` header. Those versions are legacy.

## Discovery

`server/discover` describes a server once the client can reach it. The spec does not define how a client finds servers.

## Authentication

Optional.

- **stdio.** Credentials come from the environment.
- **HTTP.** A subset of OAuth 2.1. The server is an OAuth resource server, and the client sends Bearer tokens. The client finds the authorization server through `/.well-known/oauth-protected-resource` (RFC 9728) and the server's metadata (RFC 8414), and sends resource indicators (RFC 8707). Clients register with a Client ID Metadata Document; Dynamic Client Registration is deprecated.

## Example

`server/discover`. Source: <https://modelcontextprotocol.io/specification/2026-07-28/server/discover>

```json
{
  "jsonrpc": "2.0",
  "id": "discover-1",
  "method": "server/discover",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientInfo": { "name": "ExampleClient", "version": "1.0.0" },
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```

```json
{
  "jsonrpc": "2.0",
  "id": "discover-1",
  "result": {
    "resultType": "complete",
    "supportedVersions": ["2026-07-28"],
    "capabilities": { "tools": {}, "resources": {} },
    "_meta": {
      "io.modelcontextprotocol/serverInfo": { "name": "ExampleServer", "version": "1.0.0" }
    },
    "instructions": "This server provides weather and resource utilities.",
    "ttlMs": 3600000,
    "cacheScope": "public"
  }
}
```

## Versions

Named by release date, `YYYY-MM-DD`. Released versions: 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25, 2026-07-28.

Every request names its version. A server that does not support it returns `UnsupportedProtocolVersionError`.

## References

- Specification: <https://modelcontextprotocol.io/specification/2026-07-28>
- Changes in 2026-07-28: <https://modelcontextprotocol.io/specification/2026-07-28/changelog>
- Repository: <https://github.com/modelcontextprotocol/modelcontextprotocol>
- Governance: <https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/GOVERNANCE.md>
