# agent-protocols

A reference for the protocols that AI agents use to talk to tools, to user interfaces, to each other and to services.

Each protocol has one folder. The folder says what the protocol connects, how a connection starts, what messages it carries and where the specification lives. Every protocol is described with the same template, from its upstream specification.

This repository holds no code that speaks any protocol. It is not an SDK, a gateway or a ranking.

[COMPARE.md](COMPARE.md) puts the protocols side by side: parties, wire, state, what each carries, discovery and authentication.

## Index

<!-- index:start -->
| Protocol | Name | Layer | Steward | Version | Status |
| --- | --- | --- | --- | --- | --- |
| [MCP](protocols/mcp/) | Model Context Protocol | context | Agentic AI Foundation (Linux Foundation) | 2026-07-28 | active |
| [A2A](protocols/a2a/) | Agent2Agent Protocol | agent | Agentic AI Foundation (Linux Foundation) | 1.0.0 | active |
| [ACP](protocols/agent-communication-protocol/) | Agent Communication Protocol | agent | Linux Foundation | 0.2.0 | merged |
| [ANP](protocols/anp/) | Agent Network Protocol | agent | ANP Open Source Community | 1.2 | active |
| [A2UI](protocols/a2ui/) | Agent-to-User Interface | interface | A2UI project | v0.9.1 | active |
| [AG-UI](protocols/ag-ui/) | Agent-User Interaction Protocol | interface | CopilotKit | 1.0 | active |
| [MCP Apps](protocols/mcp-apps/) | MCP Apps | interface | Agentic AI Foundation (Linux Foundation) | 2026-01-26 | active |
| [ACP](protocols/agent-client-protocol/) | Agent Client Protocol | client | Zed Industries and JetBrains | 1 | active |
| [Agent Protocol](protocols/langchain-agent-protocol/) | Agent Protocol | host | LangChain | 0.1.6 | active |
| [AHP](protocols/ahp/) | Agent Host Protocol | host | Microsoft | 1.0.0 | active |
| [Agent Protocol](protocols/agi-agent-protocol/) | Agent Protocol | task | AGI, Inc. | v1 | dormant |
| [ACP](protocols/agentic-commerce-protocol/) | Agentic Commerce Protocol | commerce | OpenAI and Stripe | 2026-04-17 | active |
| [AP2](protocols/ap2/) | Agent Payments Protocol | commerce | FIDO Alliance | 0.2.0 | active |
| [UCP](protocols/ucp/) | Universal Commerce Protocol | commerce | UCP Governing Council | 2026-08-25 | active |
<!-- index:end -->

## Layers

A protocol's layer names the two parties it sits between.

| Layer | Between |
| --- | --- |
| context | An agent or model, and the tools and data it uses. |
| agent | Two agents. |
| interface | An agent, and the user interface that shows it. |
| client | An editor or other client, and a coding agent it runs. |
| host | Clients, and a host that runs agent sessions and keeps their state. |
| task | A client, and an agent it starts tasks on. |
| commerce | An agent, and a merchant or payment provider. |

## Names that clash

Some abbreviations name more than one protocol. Each folder is named for one protocol only.

| Name | Protocol | Folder |
| --- | --- | --- |
| ACP | Agent Client Protocol, from Zed. Editors and coding agents. | [agent-client-protocol](protocols/agent-client-protocol/) |
| ACP | Agent Communication Protocol, from IBM Research. Agent to agent, merged into A2A. | [agent-communication-protocol](protocols/agent-communication-protocol/) |
| ACP | Agentic Commerce Protocol, from OpenAI and Stripe. Agent checkout. | [agentic-commerce-protocol](protocols/agentic-commerce-protocol/) |
| Agent Protocol | The REST API for tasks and steps, now kept by AGI, Inc. | [agi-agent-protocol](protocols/agi-agent-protocol/) |
| Agent Protocol | LangChain's REST API for serving agents: runs, threads, store and streaming. | [langchain-agent-protocol](protocols/langchain-agent-protocol/) |

"Agent protocol" is also used for agent protocols in general. Here it names only these two.

## Layout

```
COMPARE.md                 the protocols side by side
protocols/<id>/README.md   how the protocol works
protocols/<id>/card.json   fixed facts: steward, version, status, links
schema/card.schema.json    the fields a card.json must have
template/                  the starting files for a new protocol
tools/index.py             checks the cards and writes the index above
```

## Adding a protocol

1. Copy `template/` to `protocols/<id>/`. The id is the abbreviation in lower case, made unique where names clash.
2. Fill in `card.json` and `README.md` from the upstream specification. Link the source of every example.
3. Set `checked` to the date you compared the card with upstream.
4. Run `tools/index.py`. It checks every card and rewrites the index.

## Rules

- Facts come from the upstream specification and repository. Blog posts and announcements are not sources.
- Every protocol gets the same template and the same depth, whoever maintains it.
- No opinions, scores or recommendations. A reader picks a protocol; this repository only describes them.
- A card whose `checked` date is old may be out of date. Upstream wins.
