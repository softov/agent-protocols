# Agent Protocol

Agent Protocol is a common REST API for talking to one agent. A client creates a task, then asks the agent to run it one step at a time, and reads the files the agent produces. It was made so that benchmarks and developer tools could drive any agent the same way.

The protocol has not changed since December 2023. The repository is not archived.

| | |
| --- | --- |
| Layer | task |
| Author | Vasek Mlejnsky (E2B) |
| Steward | AGI, Inc. |
| Version | v1 |
| Status | dormant |
| Spec | <https://github.com/agi-inc/agent-protocol/blob/main/schemas/openapi.yml> |
| Repository | <https://github.com/agi-inc/agent-protocol> |
| Schema | <https://github.com/agi-inc/agent-protocol/blob/main/schemas/openapi.yml> |
| License | MIT |

The project was hosted by the AI Engineer Foundation and later moved to AGI, Inc. The old repository address redirects to the new one. The domain agentprotocol.ai no longer hosts its documentation.

## Roles

- **Client.** A user, a benchmark or a developer tool.
- **Agent.** Serves the API.

## Transport

HTTP.

## Messages

REST with JSON bodies, described in OpenAPI 3.0. Files are uploaded as multipart. All paths start with `/ap/v1/`.

Objects: **Task**, **Step**, **Artifact**.

Endpoints:

- `POST /ap/v1/agent/tasks`, `GET /ap/v1/agent/tasks`, `GET /ap/v1/agent/tasks/{task_id}`
- `POST /ap/v1/agent/tasks/{task_id}/steps`, `GET /ap/v1/agent/tasks/{task_id}/steps`, `GET /ap/v1/agent/tasks/{task_id}/steps/{step_id}`
- `POST /ap/v1/agent/tasks/{task_id}/artifacts`, `GET /ap/v1/agent/tasks/{task_id}/artifacts`, `GET /ap/v1/agent/tasks/{task_id}/artifacts/{artifact_id}`

## Connection

There is no handshake. The client creates a task with its input. Each `POST` to the task's steps runs the next step and returns it. The client repeats until a step is marked as the last.

## Discovery

None defined.

## Authentication

None defined.

## Example

Create a task. The spec has no complete example exchange; these bodies are built from the `example` values in the OpenAPI schema. Source: <https://github.com/agi-inc/agent-protocol/blob/main/schemas/openapi.yml>, `TaskRequestBody` and `Task`.

```http
POST /ap/v1/agent/tasks
Content-Type: application/json

{
  "input": "Write 'Washington' to the file 'output.txt'.",
  "additional_input": { "debug": false, "mode": "benchmarks" }
}
```

```json
{
  "task_id": "50da533e-3904-4401-8a07-c49adf88b5eb",
  "input": "Write 'Washington' to the file 'output.txt'.",
  "additional_input": { "debug": false, "mode": "benchmarks" },
  "artifacts": []
}
```

## Versions

The version is in the path, `v1`. The SDKs and clients have their own SemVer releases.

## References

- Specification: <https://github.com/agi-inc/agent-protocol/blob/main/schemas/openapi.yml>
- Repository: <https://github.com/agi-inc/agent-protocol>
