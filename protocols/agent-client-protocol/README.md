# Agent Client Protocol (ACP)

The Agent Client Protocol connects a code editor to an AI coding agent. The editor starts the agent as a subprocess and talks to it over stdio. The editor sends prompts; the agent streams back its work and calls back into the editor to read and write files, run terminals and ask the user for permission. It does for coding agents what the Language Server Protocol does for language tools: any editor that speaks it can run any agent that speaks it.

Two other protocols use the abbreviation ACP: the [Agent Communication Protocol](../agent-communication-protocol/) and the [Agentic Commerce Protocol](../agentic-commerce-protocol/).

| | |
| --- | --- |
| Layer | client |
| Author | Zed Industries |
| Steward | Zed Industries and JetBrains |
| Version | 1 |
| Status | active |
| Spec | <https://agentclientprotocol.com/protocol/v1/overview> |
| Repository | <https://github.com/agentclientprotocol/agent-client-protocol> |
| Schema | <https://github.com/agentclientprotocol/agent-client-protocol/blob/main/schema/v1/schema.json> |
| License | Apache-2.0 |

## Roles

- **Client.** The editor. It starts the agent, owns the files and terminals, and shows the user what the agent does.
- **Agent.** The coding agent. It takes prompts and does the work.

Both sides send requests.

## Transport

stdio. The client launches the agent as a subprocess. Messages are newline-delimited JSON on stdin and stdout; stderr is for logs. Custom transports are allowed. A Streamable HTTP transport is a draft proposal.

## Messages

JSON-RPC 2.0 in UTF-8. Cancellation uses `$/cancel_request`.

Agent methods, called by the client:

- `initialize`, `authenticate`, `logout`
- `session/new`, `session/load`, `session/list`, `session/resume`, `session/close`, `session/delete`
- `session/prompt`, `session/cancel`
- `session/set_mode`, `session/set_config_option`

Client methods, called by the agent:

- `session/update` - a notification with the agent's progress: message chunks, tool calls, plans.
- `session/request_permission` - ask the user to allow a tool call.
- `fs/read_text_file`, `fs/write_text_file`
- `terminal/create`, `terminal/output`, `terminal/wait_for_exit`, `terminal/kill`, `terminal/release`
- `elicitation/create`, `elicitation/complete`

The client can pass MCP servers to the agent when it creates a session.

## Connection

1. The client starts the agent process.
2. The client sends `initialize` with its protocol version, capabilities and identity. The agent answers with its own, and with the authentication methods it accepts.
3. The client calls `authenticate` if the agent needs it.
4. The client creates a session with `session/new`, or reopens one with `session/load`.
5. Each `session/prompt` is one turn. The agent streams `session/update` notifications and calls client methods as it works, and the prompt request returns when the turn ends.

## Discovery

The ACP Registry lists agents with their install metadata: <https://cdn.agentclientprotocol.com/registry/v1/latest/registry.json>.

## Authentication

The agent lists its methods in `authMethods` in the `initialize` response. Either the agent handles the login when the client calls `authenticate` with a method id, or the client runs the agent's login program in a terminal and then starts the agent again.

## Example

`initialize`. Source: <https://agentclientprotocol.com/protocol/v1/initialization>

```json
{
  "jsonrpc": "2.0",
  "id": 0,
  "method": "initialize",
  "params": {
    "protocolVersion": 1,
    "clientCapabilities": {
      "fs": { "readTextFile": true, "writeTextFile": true },
      "terminal": true
    },
    "clientInfo": { "name": "my-client", "title": "My Client", "version": "1.0.0" }
  }
}
```

```json
{
  "jsonrpc": "2.0",
  "id": 0,
  "result": {
    "protocolVersion": 1,
    "agentCapabilities": {
      "loadSession": true,
      "promptCapabilities": { "image": true, "audio": true, "embeddedContext": true },
      "mcpCapabilities": { "http": true, "sse": true }
    },
    "agentInfo": { "name": "my-agent", "title": "My Agent", "version": "1.0.0" },
    "authMethods": []
  }
}
```

## Versions

The protocol version is one integer, raised only for breaking changes, and agreed in `initialize`. New features arrive as capabilities within a version. Version 2 is a draft. The schema and the SDKs have their own release numbers.

## References

- Specification: <https://agentclientprotocol.com/protocol/v1/overview>
- Repository: <https://github.com/agentclientprotocol/agent-client-protocol>
- Governance: <https://agentclientprotocol.com/community/governance>
- Registry: <https://github.com/agentclientprotocol/registry>
