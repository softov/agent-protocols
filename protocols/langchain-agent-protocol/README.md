# Agent Protocol (LangChain)

LangChain's Agent Protocol is a REST API for serving agents. A server hosts one or more agents. Clients start runs on them, keep multi-turn conversations in threads whose state the server stores, read long-term memory from a store, and stream output while a run is in progress. The API does not depend on any agent framework.

LangGraph Platform implements a superset of the protocol. A protocol from AGI, Inc. has the same name: see [Agent Protocol (AGI, Inc.)](../agi-agent-protocol/).

| | |
| --- | --- |
| Layer | host |
| Author | LangChain |
| Steward | LangChain |
| Version | 0.1.6 |
| Status | active |
| Spec | <https://langchain-ai.github.io/agent-protocol/api.html> |
| Repository | <https://github.com/langchain-ai/agent-protocol> |
| Schema | <https://github.com/langchain-ai/agent-protocol/blob/main/openapi.json> |
| License | MIT |

## Roles

- **Client.** An application, a user interface or another agent.
- **Server.** Hosts agents, runs them, and stores threads and memory.

## Transport

HTTP with JSON. Output streams over Server-Sent Events. The streaming protocol also runs over WebSocket and in process.

## Messages

REST, described in OpenAPI 3.1. Five groups:

- **Agents.** `POST /agents/search`, `GET /agents/{agent_id}`, `GET /agents/{agent_id}/schemas`. An agent's input, output, state and config schemas are JSON Schema.
- **Threads.** `POST /threads`, `POST /threads/search`, `GET`, `PATCH` and `DELETE /threads/{thread_id}`, `GET /threads/{thread_id}/history`, `POST /threads/{thread_id}/copy`. Each change to a thread's state adds a revision to its history. Thread status is `idle`, `busy`, `interrupted` or `error`.
- **Runs.** `POST /runs`, `POST /runs/wait`, `POST /runs/stream`, `POST /runs/search`, `GET` and `DELETE /runs/{run_id}`, `GET /runs/{run_id}/wait`, `GET /runs/{run_id}/stream`, `POST /runs/{run_id}/cancel`. A run without a `thread_id` is stateless: its thread is deleted when it completes, unless `on_completion` is `keep`. Run status is `pending`, `error`, `success`, `timeout` or `interrupted`. Only one run per thread is active at a time.
- **Store.** `PUT`, `GET` and `DELETE /store/items`, `POST /store/items/search`, `POST /store/namespaces`. Items are kept by namespace and key.
- **Streaming.** `POST /threads/{thread_id}/stream`, `GET /threads/{thread_id}/stream`, `POST /threads/{thread_id}/commands`.

Thread values may include a `messages` field, in a message format that is a subset of those used by the major model providers.

The streaming protocol has its own schema, in CDDL (RFC 8610). It is marked draft, version 0.0.13. Clients send commands with an `id`, a `method` and `params`. The server returns a success or error response with the same `id`, and pushes events with a sequence number. Events are split into channels, such as `messages`, `updates` and `lifecycle`, and are scoped by namespace, which marks a position in a tree of nested agents.

## Connection

There is no handshake.

1. Optionally, list the agents and read their schemas.
2. Create a thread.
3. Start a run on it. Wait for the output, stream it, or poll the run.
4. Start more runs on the same thread for more turns.

For one-shot work, `POST /runs/wait` or `POST /runs/stream` runs without a lasting thread.

To stream over SSE, the client opens `POST /threads/{thread_id}/stream` with the channels and namespaces it wants, and sends commands to `POST /threads/{thread_id}/commands`. Over WebSocket, `GET /threads/{thread_id}/stream` upgrades the connection, and commands and events share it. A client that reconnects asks for missed events by sequence number.

## Discovery

None defined. `POST /agents/search` lists the agents on a known server.

## Authentication

None defined.

## Example

A one-shot run. Source: <https://github.com/langchain-ai/agent-protocol/blob/main/README.md>, "Journey 2". The source gives no response body. The response is a `RunWaitResponse`, with `run`, `values` and `messages`.

```http
POST /runs/wait
Content-Type: application/json

{
  "input": {
    "prompt": "What's the fastest route to the airport?"
  },
  "metadata": {
    "useCase": "travelPlan"
  },
  "config": {
    "tags": ["ephemeral", "demo"]
  }
}
```

## Versions

SemVer, in the `info.version` field of the OpenAPI file. The streaming schema has its own version. The generated bindings are released as `langchain-protocol`.

## References

- Specification: <https://langchain-ai.github.io/agent-protocol/api.html>
- OpenAPI: <https://langchain-ai.github.io/agent-protocol/openapi.json>
- Streaming: <https://github.com/langchain-ai/agent-protocol/tree/main/streaming>
- Repository: <https://github.com/langchain-ai/agent-protocol>
