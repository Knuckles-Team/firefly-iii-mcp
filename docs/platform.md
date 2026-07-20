# Backing platform — Firefly III

`firefly-iii-mcp` is a client of an operator-managed Firefly III instance. This
repository intentionally does not package a platform deployment, database password,
instance URL, local volume path, or customized schema.

Provision and maintain Firefly III using its upstream deployment documentation and
your organization's database, backup, identity, TLS, and secret-management standards.
Then supply only the selected HTTPS API endpoint and least-privilege credential through
runtime AgentConfig as described in [Configuration, trust, and privacy](configuration.md).

Before connecting this package, verify that the platform:

- presents a complete, trusted certificate chain;
- exposes only the network routes required by the connector;
- issues a credential scoped to the enabled tool domains;
- has backup, retention, and deletion controls appropriate for financial data;
- supports the chosen identity delegation and audit policy;
- does not export record content to telemetry without explicit approval.
