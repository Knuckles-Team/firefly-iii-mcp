# Configuration, trust, and privacy

`firefly-iii-mcp` contains connection code and neutral capability metadata only.
Every endpoint, credential, identity-provider value, trust profile, tenant decision,
and observability destination is supplied at runtime. The package does not ship an
instance profile or a customized Firefly III ontology.

## Configuration boundary

The connector reads runtime values through the Agent Utilities configuration layer.
For a standalone process, inject values through its process environment. When GraphOS
launches the connector, keep `mcp_config.json` reference-only and let the MCP fleet
secret resolver project aliases into the child process.

| Setting | Purpose | Durable value |
| --- | --- | --- |
| `FIREFLY_III_URL` | HTTPS base URL of the selected Firefly III API | No packaged default; resolve at runtime |
| `FIREFLY_III_TOKEN` | Fixed bearer credential when OIDC delegation is inactive | Runtime secret only |
| `TLS_PROFILE` / `TLS_PROFILES_REF` | Verified system/private trust selection | Runtime reference only |

`mcp_config.json` uses `env://FIREFLY_III_URL` and
`env://FIREFLY_III_TOKEN`. A launcher may populate those aliases directly or map the
credential alias through AgentConfig's `MCP_FLEET_SECRET_REFS` to an approved
`env://`, `vault://`, or `secret://` source. Never replace a reference with a token or
endpoint in a checked-in file.

The default tool surface is `MCP_TOOL_MODE=condensed`. Domain toggles default to
enabled and may be disabled by the deployment. Network transports must also apply the
authentication and authorization policy selected for the MCP server.

## Authentication

The connector has two current authentication paths:

1. OIDC delegation exchanges the request-scoped user token through the shared RFC
   8693 implementation and creates a request-specific Firefly III client.
2. Without delegation, `FIREFLY_III_TOKEN` supplies the fixed service credential.

No token, subject, email address, endpoint, or exception body is written to logs.
Prefer delegation when the target and identity provider support it; otherwise scope
the fixed token to the smallest operational role the enabled tools require. Supply
OIDC client credentials through runtime references such as `OIDC_CLIENT_SECRET_REF`.

## TLS trust

Firefly III endpoints must use HTTPS. Peer and hostname verification are mandatory.
The HTTP session is configured through
`resolve_configured_tls_profile("firefly_iii")`; there is no boolean verification
control and per-request trust overrides are rejected.

System trust works without additional configuration. For a private certificate
authority, keep a complete-chain PEM bundle or mTLS material in the runtime trust
store, place the catalog behind `TLS_PROFILES_REF`, and select `TLS_PROFILE` for this
connector process. Standard runtime trust variables are honored by the shared
resolver. Do not commit certificate material or machine paths, and do not disable
verification to compensate for an incomplete server chain.

## Knowledge-graph capability

The package contributes human-reviewed inputs for the central capability compiler:

- the Firefly III finance ontology in `firefly_iii_mcp/ontology/`;
- neutral accounts, transactions, and budgets source presets in
  `firefly_iii_mcp/connectors/`;
- one comprehensive provider skill and canonical prompt sources;
- package entry points proving distribution ownership of those assets.

These inputs describe the public Firefly III model and tool surface only. The committed
release-generated bundle adds exact local tool-schema fingerprints, a signed manifest,
SHACL shapes, neutral mappings and fixtures, a migration ledger, and an offline source
attestation. It contains no instance URL, record, tenant mapping, local path, or
external-live claim. The connector deliberately exposes no direct graph-write tool;
missing or stale evidence fails closed.

Finance records can contain account identifiers, balances, descriptions, amounts,
dates, attachments, and user data. Enable source synchronization only with an approved
tenant, ACL, classification, retention, provenance, redaction, and deletion policy.

## Observability and privacy

Telemetry is disabled in the checked-in example. When OTLP or Langfuse is enabled:

- use credential and TLS-profile references;
- keep `LANGFUSE_CAPTURE_CONTENT=false` unless a separately approved policy permits
  content capture;
- use opaque run, actor, and tenant references;
- export status, counts, timing, and bounded error classes rather than prompts,
  responses, tool payloads, finance records, filesystem paths, or credentials.

## Validation

After runtime configuration is injected, validate the shared boundary without
printing resolved values:

```bash
agent-utilities-doctor --only config transport_security mcp_fleet_secrets mcp_fleet
```

Use `agent-utilities-doctor --live` only when bounded calls to the configured service
and observability backends are authorized.
