# Agent-to-User Interface (A2UI)

A2UI lets an agent describe a user interface as data instead of code. The agent streams messages that create a surface, place components on it and fill a data model. The client draws the surface with its own native components, chosen from a catalog it trusts, so the agent never sends executable code. User actions go back to the agent as messages.

A2UI does not carry itself. It rides inside another protocol, such as A2A or AG-UI.

| | |
| --- | --- |
| Layer | interface |
| Author | Google |
| Steward | A2UI project |
| Version | v0.9.1 (2026-05-29) |
| Status | active, public preview |
| Spec | <https://a2ui.org/specification/v0.9.1-a2ui/> |
| Repository | <https://github.com/a2ui-project/a2ui> |
| Schema | <https://github.com/a2ui-project/a2ui/tree/main/specification/v0_9_1/json> |
| License | Apache-2.0 |

## Roles

- **Server.** The agent. It describes surfaces and updates them.
- **Client.** The renderer. It owns a catalog of components and draws what the server describes.

## Transport

Not defined by A2UI. The spec gives bindings for A2A, where each A2UI message is one part of an A2A message and the A2A `contextId` is the session, and for AG-UI. It lists MCP, Server-Sent Events, WebSocket and REST as other carriers. Framing belongs to the carrier.

## Messages

A stream of JSON envelopes, often as JSON Lines. MIME type `application/a2ui+json`. Every message carries a `version` field.

Server to client:

- `createSurface` - start a surface and name the component catalog it uses.
- `updateComponents` - set components, as a flat list linked by id.
- `updateDataModel` - set values at a path in the surface's data model.
- `deleteSurface` - remove a surface.

Client to server:

- `action` - a user action on a component, with its context.
- `error` - a rendering error.

## Connection

There is no A2UI handshake. The server sends `createSurface`, then `updateComponents` and `updateDataModel` as often as it needs, and finally `deleteSurface`. Components bind to paths in the data model, so a data update changes the view without resending components.

## Discovery

Through the carrier. The server lists its catalogs in its capabilities, for example in an A2A Agent Card. The client sends `a2uiClientCapabilities`, with the catalogs it supports, in the metadata of each A2A message.

## Authentication

None defined. It belongs to the carrier.

## Example

Shortened. Source: <https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md>, "Example Stream".

```json
{"version": "v0.9.1", "createSurface": {"surfaceId": "contact_form_1", "catalogId": "https://a2ui.org/specification/v0_9_1/catalogs/basic/catalog.json"}}
{"version": "v0.9.1", "updateComponents": {"surfaceId": "contact_form_1", "components": [{"id": "root", "component": "Card", "child": "form_container"}]}}
{"version": "v0.9.1", "updateDataModel": {"surfaceId": "contact_form_1", "path": "/contact", "value": {"firstName": "John", "lastName": "Doe", "email": "john.doe@example.com"}}}
{"version": "v0.9.1", "deleteSurface": {"surfaceId": "contact_form_1"}}
```

## Versions

Versions are named `vMAJOR.MINOR.PATCH` and carried in every message. v0.9.1 is the current release and is closed to changes. v1.0 is a release candidate. v0.8 is legacy.

## References

- Specification: <https://a2ui.org/specification/v0.9.1-a2ui/>
- Repository: <https://github.com/a2ui-project/a2ui>
