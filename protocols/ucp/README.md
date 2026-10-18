# Universal Commerce Protocol (UCP)

UCP connects agents and apps to businesses for the whole of a purchase: catalog search, cart, checkout, orders, account linking and payment. Each party publishes a profile that lists what it supports. For each session the two sides use what both profiles have in common. UCP runs over REST, MCP, A2A or an embedded protocol.

| | |
| --- | --- |
| Layer | commerce |
| Author | Google and Shopify |
| Steward | UCP Governing Council |
| Version | 2026-08-25 (2026-08-25) |
| Status | active |
| Spec | <https://ucp.dev/latest/specification/overview/> |
| Repository | <https://github.com/Universal-Commerce-Protocol/ucp> |
| Schema | <https://github.com/Universal-Commerce-Protocol/ucp/tree/v2026-08-25/source/schemas> |
| License | Apache-2.0 |

The Governing Council owns all UCP assets. Google and Shopify hold permanent seats; other seats are elected. Domain councils cover shopping, food, lodging and payments.

## Roles

- **Platform.** The agent or app acting for the buyer.
- **Business.** The seller.
- **Payment service provider** and **credential provider.** Handle payment and payment tokens.

## Transport

Each party lists its transports in the `services` section of its profile.

- **REST.** HTTP/1.1 or later, JSON.
- **MCP.** Operations as MCP tools.
- **A2A.** Operations as A2A messages.
- **Embedded Protocol.** JSON-RPC 2.0 for a business checkout embedded in the platform.

## Messages

JSON. Amounts are in minor units; dates are RFC 3339. Capabilities have reverse-DNS names, such as `dev.ucp.shopping.checkout`, and their own versions.

Shopping capabilities: catalog search and lookup, cart, checkout, and orders. Extensions add discounts and fulfillment. Payment handlers, such as `com.google.pay`, describe how a payment is made.

Checkout over REST:

- `POST /checkout-sessions`
- `GET /checkout-sessions/{id}`
- `PUT /checkout-sessions/{id}`
- `POST /checkout-sessions/{id}/complete`
- `POST /checkout-sessions/{id}/cancel`

Every response carries a `ucp` object with the version, the capabilities in use and the payment handlers.

## Connection

1. The platform reads the business profile.
2. On each request the platform names its own profile URL in the `UCP-Agent` header.
3. The business intersects the two profiles and uses only the capabilities both support.
4. The checkout runs through the operations above.
5. The business sends order updates to the platform by signed webhook.

## Discovery

The business profile at `/.well-known/ucp`. It lists services, capabilities, payment handlers and signing keys (JWK).

## Authentication

API keys, OAuth 2.0, mutual TLS, or RFC 9421 HTTP Message Signatures. Signature keys come from the signer's profile, so a platform can start without registering first. Webhooks from the business must be signed. Account linking uses OAuth 2.0. AP2 mandates are an extension for purchases the user is not present for.

## Example

Cancel a checkout, shortened. Source: <https://github.com/Universal-Commerce-Protocol/ucp/blob/v2026-08-25/docs/specification/shopping/checkout/rest.md>, "Cancel Checkout". The `{{ ucp_version }}` placeholders are in the source.

```http
POST /checkout-sessions/{id}/cancel
UCP-Agent: profile="https://platform.example/profile"
Content-Type: application/json

{}
```

```json
{
  "ucp": {
    "version": "{{ ucp_version }}",
    "capabilities": {
      "dev.ucp.shopping.checkout": [{ "version": "{{ ucp_version }}" }]
    }
  },
  "id": "chk_123456789",
  "status": "canceled",
  "currency": "USD",
  "line_items": [
    {
      "id": "li_1",
      "item": { "id": "item_123", "title": "Red T-Shirt", "price": 2500 },
      "quantity": 2,
      "totals": [
        { "type": "subtotal", "amount": 5000 },
        { "type": "total", "amount": 5000 }
      ]
    }
  ],
  "totals": [
    { "type": "subtotal", "amount": 5000 },
    { "type": "tax", "amount": 400 },
    { "type": "total", "amount": 5400 }
  ]
}
```

## Versions

Named by release date, `YYYY-MM-DD`, tagged `vYYYY-MM-DD`. Releases: 2026-01-11, 2026-01-23, 2026-04-08, 2026-08-25. Since 2026-08-25 each capability also has its own version.

## References

- Specification: <https://ucp.dev/latest/specification/overview/>
- Repository: <https://github.com/Universal-Commerce-Protocol/ucp>
- Governance: <https://github.com/Universal-Commerce-Protocol/.github/blob/main/GOVERNANCE.md>
