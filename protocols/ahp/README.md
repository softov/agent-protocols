# Agent Host Protocol (AHP)

AHP connects clients to an agent host. The host runs agent sessions and owns their state. Any number of clients connect to the same host and see the same sessions at the same time. State is a set of immutable values changed only by actions, and every client applies the same actions through the same reducers, so all clients converge on one view.

| | |
| --- | --- |
| Layer | host |
| Author | Microsoft |
| Steward | Microsoft |
| Version | 1.0.0 (2026-10-02) |
| Status | active |
| Spec | <https://microsoft.github.io/agent-host-protocol/> |
| Repository | <https://github.com/microsoft/agent-host-protocol> |
| Schema | <https://github.com/microsoft/agent-host-protocol/tree/main/schema> |
| License | MIT |

## Roles

- **Server (agent host).** Runs the agents, holds the state of every session, chat and terminal, and is the only authority on that state.
- **Client.** A user interface: an editor, a terminal client, a mobile app. It subscribes to the state it shows and dispatches actions to change it.

The VS Code agent host is the reference server.

## Transport

The spec does not prescribe a transport. Any stream that is reliable, ordered, bidirectional and delivers whole messages is acceptable. Client and server agree on it before the protocol starts.

WebSocket is the common choice. The server is the WebSocket server, and each text frame carries exactly one JSON-RPC message.

## Messages

JSON-RPC 2.0. Every command and notification carries `params.channel`, a URI that names the state it applies to, so a peer can route any message on `(method, params.channel)` alone.

Channels:

- `ahp-root://` - global state: agents, terminals, host configuration. Always present.
- `ahp-session:/<uuid>` - one session and its catalog of chats.
- `ahp-chat:/<cid>` - one conversation: turns, streaming output, tool calls, input requests.
- `ahp-terminal:/<id>` - one terminal.
- `ahp-changeset:/<id>` - one set of file changes.
- `ahp-automations://`, `ahp-canvas:/<id>`, `ahp-resource-watch:/<id>`, `ahp-otlp:` - automations, canvases, file watches and telemetry.

Message kinds:

- **Commands** (requests). `initialize`, `reconnect`, `subscribe`, `createSession`, `disposeSession`, `listSessions`, `fetchTurns`, `authenticate`, `ping`, and the `resource*` file operations.
- **Actions.** State changes. The server pushes them in the `action` notification with a `serverSeq`. A client sends its own with the `dispatchAction` notification and a `clientSeq`, and applies it locally before the server confirms it.
- **Protocol notifications.** `root/sessionAdded`, `root/sessionRemoved`, `auth/required` and others.
- **Server to client requests.** The server can call the `resource*` operations on the client, to read and write the client's files.

Tools come from both sides. The session state lists the host's tools in `serverTools`. A client joins a session as an active client with `session/activeClientSet` and publishes its own tools there; when the agent calls one, that client runs it and reports the result. User messages can carry attachments, either inline as base64 data or as a URI the agent reads with `resourceRead`.

A sub-agent is a chat of its own. The tool call that spawns it returns the worker chat's URI, and the worker chat records that tool call as its origin. A worker chat can be read-only or hidden from the user. Sub-agents and background shells that outlive a turn are listed in the parent chat's state.

Names that start with `x-` are reserved for implementation extensions.

## Connection

1. The client opens the transport.
2. The client sends `initialize` with the protocol versions it speaks, a `clientId`, and optionally the channels to subscribe to at once.
3. The server picks a version and replies with it, its current `serverSeq`, and a snapshot of each channel subscribed.
4. From then on the client subscribes and unsubscribes channels, sends commands and dispatches actions. The server streams actions for every subscribed channel.
5. After a dropped connection the client sends `reconnect` with its `clientId` and the last `serverSeq` it saw, and the server replays what it missed or sends fresh snapshots.

## Discovery

None defined. The client reaches the host at an address agreed out of band. Once connected, the agents the host offers are listed in the state of `ahp-root://`.

## Authentication

Two levels.

- **Connection.** Out of scope for the protocol. The spec recommends gating it in the transport handshake, for example in the WebSocket upgrade request.
- **Agents and their resources.** Each agent lists the resources it needs a token for in `AgentInfo.protectedResources`, in the RFC 9728 protected resource metadata format. The client gets a token from the named authorization server with standard OAuth 2.0 and pushes it with the `authenticate` command. The server asks for a new token with the `auth/required` notification.

## Example

Handshake, shortened. Source: <https://github.com/microsoft/agent-host-protocol/blob/main/docs/specification/lifecycle.md>

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "channel": "ahp-root://",
    "protocolVersions": ["0.3.0"],
    "clientId": "client-abc",
    "clientInfo": { "name": "acme-ide", "version": "2.5.0" },
    "initialSubscriptions": ["ahp-root://"],
    "locale": "en-US"
  }
}
```

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "0.3.0",
    "serverSeq": 42,
    "serverInfo": { "name": "acme-agent-host", "version": "1.4.2" },
    "defaultDirectory": "file:///home/testuser",
    "snapshots": [
      {
        "resource": "ahp-root://",
        "state": { "agents": [] },
        "fromSeq": 42
      }
    ]
  }
}
```

A server action on a chat channel. Source: <https://github.com/microsoft/agent-host-protocol/blob/main/docs/specification/subscriptions.md>

```json
{
  "jsonrpc": "2.0",
  "method": "action",
  "params": {
    "channel": "ahp-chat:/<cid>",
    "action": { "type": "chat/delta", "turnId": "t1", "partId": "p1", "content": "Hello" },
    "serverSeq": 6,
    "origin": { "clientId": "client-1", "clientSeq": 1 }
  }
}
```

## Versions

SemVer, `MAJOR.MINOR.PATCH`, with no pre-release or build suffix. The spec and each language SDK are released separately; spec releases are tagged `spec/vX.Y.Z`.

The client offers a list of versions in `initialize`. The server picks the highest one inside a range it supports and returns it, or fails with `UnsupportedProtocolVersion` (`-32005`) and the list of versions it supports. The released baselines are 1.0.0 and 0.9.0.

## References

- Specification: <https://microsoft.github.io/agent-host-protocol/>
- Repository: <https://github.com/microsoft/agent-host-protocol>
- Changelog: <https://github.com/microsoft/agent-host-protocol/blob/main/CHANGELOG.md>
- Reference server: <https://github.com/microsoft/vscode/tree/main/src/vs/platform/agentHost/node>
