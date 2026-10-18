# Agent-User Interaction Protocol (AG-UI)

AG-UI connects an agent backend to the application a user sees. The application sends one request to start a run. The agent answers with one ordered stream of typed events: text as it is generated, tool calls, state changes, and the start and end of the run. The application builds its view from those events.

| | |
| --- | --- |
| Layer | interface |
| Author | CopilotKit |
| Steward | CopilotKit |
| Version | 1.0 (2026-09-17) |
| Status | active |
| Spec | <https://docs.ag-ui.com/spec/1.0> |
| Repository | <https://github.com/ag-ui-protocol/ag-ui> |
| Schema | <https://github.com/ag-ui-protocol/ag-ui/blob/main/spec/1.0/schema.json> |
| License | MIT |

## Roles

- **Producer.** The agent backend. It runs the agent and emits events.
- **Consumer.** The user-facing application. It starts runs and renders the events.

## Transport

- **HTTP with Server-Sent Events.** The default binding. The consumer POSTs the run input and reads the response as an event stream.
- **HTTP with Protocol Buffers.** A binary binding, media type `application/vnd.ag-ui.event+proto`.

Custom bindings are allowed if they meet the binding contract in the spec.

## Messages

The request is one `RunAgentInput` JSON object: `threadId`, `runId`, `messages`, `state`, `tools` and `protocolVersion`.

The response is a stream of JSON events, one per SSE `data` field, told apart by `type`. Version 1.0 defines 31 event types in eight families:

- **Lifecycle.** `RUN_STARTED`, `RUN_FINISHED`, `RUN_ERROR`, `STEP_STARTED`, `STEP_FINISHED`.
- **Text messages.** `TEXT_MESSAGE_START`, `TEXT_MESSAGE_CONTENT`, `TEXT_MESSAGE_END` and related.
- **Tool calls.** `TOOL_CALL_START`, `TOOL_CALL_ARGS`, `TOOL_CALL_END` and related.
- **Reasoning.** `REASONING_*`.
- **State.** `STATE_SNAPSHOT`, `STATE_DELTA` (a JSON Patch), `MESSAGES_SNAPSHOT`.
- **Activity.** `ACTIVITY_SNAPSHOT`, `ACTIVITY_DELTA`.
- **Subagents.** `SUBAGENT_STARTED`, `SUBAGENT_FINISHED`, `SUBAGENT_ERROR`.
- **Passthrough.** `RAW`, `CUSTOM`.

Only the run lifecycle events are mandatory.

## Connection

There is no handshake. One request is one run.

1. The consumer POSTs `RunAgentInput`.
2. The producer opens the stream with `RUN_STARTED`.
3. It sends events as the run goes on.
4. It closes the run with `RUN_FINISHED` or `RUN_ERROR`.

A broken stream cannot be resumed.

## Discovery

None defined. The spec defines an `AgentCapabilities` declaration (identity, transport, tools, state, multiple agents, reasoning, multimodal input) but no way for a consumer to fetch it, and no binding in 1.0 carries it.

## Authentication

None in the protocol. Authentication belongs to the binding, for example HTTP authentication. A refused request gets an HTTP error status before the stream opens.

## Example

Source: <https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse>

```http
POST /agent HTTP/1.1
Content-Type: application/json
Accept: text/event-stream

{"threadId":"thr-1","runId":"run-1","messages":[…]}
```

```http
HTTP/1.1 200 OK
Content-Type: text/event-stream

data: {"type":"RUN_STARTED","threadId":"thr-1","runId":"run-1"}

data: {"type":"TEXT_MESSAGE_START","messageId":"msg-1","role":"assistant"}

data: {"type":"TEXT_MESSAGE_CONTENT","messageId":"msg-1","delta":"Hello."}

data: {"type":"TEXT_MESSAGE_END","messageId":"msg-1"}

data: {"type":"RUN_FINISHED","threadId":"thr-1","runId":"run-1"}
```

## Versions

The spec is versioned `MAJOR.MINOR`, in folders such as `spec/1.0` and `spec/draft`. Version 1.0 was frozen on 2026-09-17; earlier releases were 0.0.x. The version travels in the run: `RunAgentInput.protocolVersion` and `RUN_STARTED.protocolVersion`.

## References

- Specification: <https://docs.ag-ui.com/spec/1.0>
- Repository: <https://github.com/ag-ui-protocol/ag-ui>
- Events: <https://docs.ag-ui.com/spec/1.0/events>
