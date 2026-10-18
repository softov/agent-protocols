# Agent2Agent Protocol (A2A)

A2A connects two agents that may be built by different vendors on different frameworks. A client agent finds a remote agent, reads what it can do, and sends it messages. The remote agent answers with a message or with a task that it works on and reports on until the task ends. Neither agent sees the other's internals.

| | |
| --- | --- |
| Layer | agent |
| Author | Google |
| Steward | Agentic AI Foundation (Linux Foundation) |
| Version | 1.0.0 (2026-03-12) |
| Status | active |
| Spec | <https://a2a-protocol.org/latest/specification/> |
| Repository | <https://github.com/a2aproject/A2A> |
| Schema | <https://github.com/a2aproject/A2A/blob/main/specification/a2a.proto> |
| License | Apache-2.0 |

## Roles

- **Client.** The agent or application that sends a request.
- **Remote agent (server).** The agent that receives it and does the work.

## Transport

The spec defines three bindings:

- **JSON-RPC 2.0** over HTTP.
- **gRPC.**
- **HTTP+JSON**, a REST mapping with media type `application/a2a+json`.

Streaming uses Server-Sent Events on JSON-RPC and REST, and server streaming on gRPC. For long tasks the remote agent can also send push notifications to a webhook the client registers. An agent declares the bindings it supports in its Agent Card. Custom bindings are allowed.

## Messages

The data model is defined in Protocol Buffers (`a2a.proto`, normative) and carried as JSON on the JSON-RPC and REST bindings. A JSON Schema is generated from it.

Objects:

- **Message.** One turn, with a role and a list of parts.
- **Part.** Text, a file, or structured data.
- **Task.** A unit of work with an id, a status and artifacts.
- **Artifact.** An output of a task.
- **Agent Card.** The agent's identity, skills, endpoints, bindings and security schemes.

Operations: `SendMessage`, `SendStreamingMessage`, `GetTask`, `ListTasks`, `CancelTask`, `SubscribeToTask`, the push notification config operations (create, get, list, delete), and `GetExtendedAgentCard`.

## Connection

There is no handshake.

1. The client gets the remote agent's Agent Card.
2. It picks a binding and a protocol version the card lists.
3. It sends a message. The answer is a message, or a task.
4. A task moves through the states submitted, working, input required, auth required, completed, failed, canceled and rejected. The client follows it by polling, by streaming or by push notification.

`contextId` groups related tasks and messages into one conversation.

## Discovery

The Agent Card. An agent publishes it at `https://{domain}/.well-known/agent-card.json`. Clients can also get cards from a registry or catalog, or by direct configuration. An authenticated client can ask for a fuller card with `GetExtendedAgentCard`.

## Authentication

At the transport. Production deployments must encrypt: HTTPS for the HTTP bindings, TLS for gRPC. The Agent Card lists the schemes the agent accepts in `securitySchemes`: API key, HTTP authentication (Bearer, Basic), OAuth 2.0 (authorization code with PKCE, client credentials, device code), OpenID Connect and mutual TLS. The client gets credentials out of band and sends them with every request. A task can enter the auth required state when it needs more credentials partway through.

## Example

`SendMessage` on the REST binding. Source: <https://a2a-protocol.org/latest/specification/>, section 6.1.

```http
POST /message:send
Content-Type: application/a2a+json
Authorization: Bearer token

{
  "message": {
    "role": "ROLE_USER",
    "parts": [{ "text": "What is the weather today?" }],
    "messageId": "msg-uuid"
  }
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/a2a+json

{
  "task": {
    "id": "task-uuid",
    "contextId": "context-uuid",
    "status": { "state": "TASK_STATE_COMPLETED" },
    "artifacts": [
      {
        "artifactId": "artifact-uuid",
        "name": "Weather Report",
        "parts": [{ "text": "Today will be sunny with a high of 75°F" }]
      }
    ]
  }
}
```

On the JSON-RPC binding the same payload is the `params` of method `SendMessage`.

## Versions

SemVer. The repository's latest release is 1.0.1 (2026-05-28), a patch to the 1.0.0 specification. Peers agree only on `MAJOR.MINOR`: the client sends it in the `A2A-Version` header or query parameter, and an empty value means 0.3.

## References

- Specification: <https://a2a-protocol.org/latest/specification/>
- Repository: <https://github.com/a2aproject/A2A>
- Changelog: <https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md>
- Governance: <https://github.com/a2aproject/A2A/blob/main/GOVERNANCE.md>
