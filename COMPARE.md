# Compare

The protocols side by side. Every cell comes from the protocol's own page in `protocols/`; where they disagree, the page wins.

Each column holds one kind of thing. A cell names what the protocol itself defines. What a protocol gets from another protocol is under [How they stack](#how-they-stack), not in the cell. A dash means the page records nothing for that column.

Rows follow the layers in the [index](README.md#index).

## Parties

Who sits on each side, and who sends requests.

| Protocol | Client side | Server side | Requests sent by |
| --- | --- | --- | --- |
| [MCP](protocols/mcp/) | Host application, one client per server | Server with tools, resources and prompts | Client only. The server asks for input by returning `input_required`. |
| [A2A](protocols/a2a/) | Client agent or application | Remote agent | Client |
| [Agent Communication Protocol](protocols/agent-communication-protocol/) | Application, person or agent | Server hosting agents | Client |
| [ANP](protocols/anp/) | Agent | Agent | Either agent |
| [AG-UI](protocols/ag-ui/) | Consumer: the user-facing application | Producer: the agent backend | Consumer, one request per run |
| [A2UI](protocols/a2ui/) | Renderer | Agent | Both, as messages: surfaces from the agent, actions from the renderer |
| [MCP Apps](protocols/mcp-apps/) | View in an iframe | MCP host, relaying to the MCP server | Both: the view sends requests, the host sends notifications |
| [Agent Client Protocol](protocols/agent-client-protocol/) | Editor | Coding agent, run as a subprocess | Both |
| [AHP](protocols/ahp/) | User interface: editor, terminal, mobile | Agent host | Both. The host can call file operations on the client. |
| [Agent Protocol (AGI)](protocols/agi-agent-protocol/) | Client, benchmark or tool | Agent | Client |
| [Agent Protocol (LangChain)](protocols/langchain-agent-protocol/) | Application, user interface or agent | Server hosting agents | Client |
| [Agentic Commerce Protocol](protocols/agentic-commerce-protocol/) | Buyer's agent | Seller, and payment provider | Agent |
| [AP2](protocols/ap2/) | Shopping agent | Merchant, credential provider, processor | None. AP2 defines signed objects, not requests. |
| [UCP](protocols/ucp/) | Platform | Business | Platform |

## Wire

| Protocol | Transport | Encoding |
| --- | --- | --- |
| MCP | stdio, Streamable HTTP | JSON-RPC 2.0 |
| A2A | HTTP, gRPC | JSON-RPC 2.0, REST JSON, Protocol Buffers |
| Agent Communication Protocol | HTTP | REST JSON |
| ANP | HTTPS, secure WebSocket | JSON-LD descriptions, JSON-RPC 2.0 messages |
| AG-UI | HTTP | SSE with JSON events, or Protocol Buffers |
| A2UI | The carrier's | JSON envelopes |
| MCP Apps | `postMessage` | JSON-RPC 2.0 |
| Agent Client Protocol | stdio | JSON-RPC 2.0 |
| AHP | Any reliable ordered stream; WebSocket in practice | JSON-RPC 2.0 |
| Agent Protocol (AGI) | HTTP | REST JSON |
| Agent Protocol (LangChain) | HTTP, WebSocket | REST JSON, SSE |
| Agentic Commerce Protocol | HTTPS | REST JSON, JSON-RPC 2.0 |
| AP2 | The carrier's | SD-JWT verifiable credentials |
| UCP | HTTP | REST JSON, JSON-RPC 2.0 |

## Sessions and state

| Protocol | Handshake | State is kept by | Server pushes | After a dropped connection |
| --- | --- | --- | --- | --- |
| MCP | None | Nobody. Handles are passed in tool arguments. | SSE per request, `subscriptions/listen` | Client resends the request with a new id |
| A2A | None | Remote agent: tasks, grouped by `contextId` | SSE, gRPC streaming, webhooks | `SubscribeToTask`, polling |
| Agent Communication Protocol | None | Server: runs, and sessions by `session_id` | SSE | - |
| ANP | None | - | - | - |
| AG-UI | None | Consumer: it sends messages and state with each run | SSE | Cannot be resumed |
| A2UI | None | Renderer: the surface's data model | - | - |
| MCP Apps | `ui/initialize` | Host | Notifications to the view | - |
| Agent Client Protocol | `initialize` | Agent: sessions | `session/update` notifications | `session/load`, `session/resume` |
| AHP | `initialize` | Host, the only authority; clients mirror it | `action` notifications per channel | `reconnect` with the last `serverSeq`; the host replays |
| Agent Protocol (AGI) | None | Agent: tasks and steps | None | - |
| Agent Protocol (LangChain) | None | Server: threads with history | SSE, WebSocket | Replay by sequence number |
| Agentic Commerce Protocol | None | Seller: checkout sessions | Webhooks | - |
| AP2 | - | - | - | - |
| UCP | None | Business: checkout sessions | Webhooks | - |

## What it carries

Commerce protocols are in the next table.

- **Tools offered.** A side gives the agent tools it can call.
- **Tool calls shown.** The agent reports the tool calls it makes.
- **Files in messages.** File content carried as part of a message.
- **File system.** One side reads or writes the other side's files.
- **Asks the user.** The agent stops to ask the user for input or permission.
- **Sub-agents.** Agents started inside a run, and how they show up.
- **Memory.** Long-term storage outside a conversation.

| Protocol | Tools offered | Tool calls shown | Files in messages | File system | Terminals | User interface | Asks the user | Sub-agents | Memory |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MCP | `tools/list`, `tools/call` | - | Resources, by URI | - | - | - | Elicitation | - | - |
| A2A | - | - | File parts, artifacts | - | - | - | Task state input required | - | - |
| Agent Communication Protocol | - | - | Parts with `content_url` | - | - | - | Run state awaiting | - | - |
| ANP | - | - | Attachments | - | - | - | - | - | - |
| AG-UI | `tools` in the run input | `TOOL_CALL_*` events | - | - | - | Events the application renders | - | `SUBAGENT_*` events | - |
| A2UI | - | - | - | - | - | Components from the renderer's catalog | - | - | - |
| MCP Apps | - | Tool input and result sent to the view | - | - | - | HTML view in a sandboxed iframe | - | - | - |
| Agent Client Protocol | MCP servers passed to the agent | `session/update` | - | `fs/read_text_file`, `fs/write_text_file` | `terminal/*` | - | `session/request_permission`, elicitation | - | - |
| AHP | Client tools, published in `activeClients`; server tools in session state | Chat state | Message attachments, inline or by URI | `resource*` operations, changesets | `ahp-terminal:/` channels | - | Input requests in chat state | Worker chats, linked to the spawning tool call | - |
| Agent Protocol (AGI) | - | - | Artifacts | - | - | - | - | - | - |
| Agent Protocol (LangChain) | - | Tool lifecycle events | - | - | - | - | Human-in-the-loop input | Namespaces in the stream | Store, by namespace and key |

## Commerce

| | [Agentic Commerce Protocol](protocols/agentic-commerce-protocol/) | [UCP](protocols/ucp/) | [AP2](protocols/ap2/) |
| --- | --- | --- | --- |
| Catalog | Product feed, pushed by the seller | Catalog search and lookup | - |
| Cart | `/carts` | Cart capability | - |
| Checkout | `/checkout_sessions` | `/checkout-sessions` | Checkout Mandate over the merchant's Checkout JWT |
| Payment | Delegated payment token from the payment provider | Payment handlers | Payment Mandate, then a token from the credential provider |
| Proof of user consent | - | - | Mandates signed by the user on a trusted surface |
| Orders | Order webhooks | Orders capability, signed webhooks | Receipts from merchant and processor |

## Discovery and authentication

- **Finding a server.** How a client learns where a server is.
- **Describing itself.** How a server tells a client what it offers.

| Protocol | Finding a server | Describing itself | Authentication |
| --- | --- | --- | --- |
| MCP | - | `server/discover` | OAuth 2.1 subset over HTTP; environment over stdio |
| A2A | `/.well-known/agent-card.json`, registries | Agent Card, `GetExtendedAgentCard` | Schemes listed in the Agent Card: API key, HTTP, OAuth 2.0, OpenID Connect, mutual TLS |
| Agent Communication Protocol | `/.well-known/agent.yml`, registries | `GET /agents`, agent manifest | - |
| ANP | `/.well-known/agent-descriptions`, search service agents | Agent Description | DID: RFC 9421 signed requests, then a Bearer token |
| AG-UI | - | - | - |
| A2UI | - | Catalogs in the carrier's capabilities | - |
| MCP Apps | - | Extension id in the host's capabilities; views in `resources/list` | - |
| Agent Client Protocol | ACP Registry | `initialize` | `authMethods` in `initialize`, then `authenticate` |
| AHP | - | `initialize`; agents in `ahp-root://` | Agent tokens by OAuth 2.0 and `authenticate`; connection out of scope |
| Agent Protocol (AGI) | - | - | - |
| Agent Protocol (LangChain) | - | `POST /agents/search`, agent schemas | - |
| Agentic Commerce Protocol | `/.well-known/acp.json` | The same document | Bearer token; HMAC-signed webhooks |
| AP2 | - | - | User credentials over OpenID4VP |
| UCP | `/.well-known/ucp` | Business profile, intersected with the platform's | API keys, OAuth 2.0, mutual TLS, RFC 9421 signatures |

## How they stack

- MCP Apps extends MCP. It is how an MCP server shows a user interface.
- A2UI rides in A2A or AG-UI. It is how those agents describe a user interface.
- AP2 rides in A2A or UCP. It is how UCP proves user consent to a payment.
- UCP runs over MCP and A2A, as well as REST.
- The Agentic Commerce Protocol runs over MCP, as well as REST.
- The Agent Client Protocol passes MCP servers to the agent.
- ANP agents can describe an interface as an MCP server, and its payments draft adapts AP2.
- A2A and ANP connect agents to agents. An agent that calls another agent is a client of it.
- The IBM Agent Communication Protocol merged into A2A.
