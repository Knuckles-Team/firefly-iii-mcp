# Deployment

`firefly-iii-mcp` exposes an MCP server and an optional A2A agent server. Keep all
service endpoints, credentials, identity settings, TLS trust, model selection, and
telemetry destinations in runtime AgentConfig or the deployment secret store.

Read [Configuration, trust, and privacy](configuration.md) before enabling a network
transport.

## Stdio

Use the checked-in `mcp_config.json` with GraphOS or another alias-aware launcher. It
contains only `env://` references. A launcher without reference resolution must omit
those environment entries and inject the runtime values itself.

```json
{
  "mcpServers": {
    "firefly-iii-mcp": {
      "command": "uvx",
      "args": ["--from", "firefly-iii-mcp[mcp]", "firefly-iii-mcp"],
      "env": {
        "MCP_TOOL_MODE": "condensed",
        "FIREFLY_III_URL": "env://FIREFLY_III_URL",
        "FIREFLY_III_TOKEN": "env://FIREFLY_III_TOKEN"
      }
    }
  }
}
```

## Network transport

Bind locally by default and place authentication, authorization, and verified TLS at
the network boundary:

```bash
firefly-iii-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

For a remote deployment, let the launcher or AgentConfig supply the authenticated
HTTPS MCP URL. Do not persist that deployment endpoint in this repository.

## Containers

Build the desired target, then inject runtime configuration through the orchestrator:

```bash
docker build --target mcp -t firefly-iii-mcp:mcp -f docker/Dockerfile .
docker build --target agent -t firefly-iii-mcp:agent-local -f docker/Dockerfile .
```

The Compose examples use operator-overridable image variables, bind published ports
to loopback, disable telemetry and the web UI by default, and require the agent's MCP
URL, provider, and model at runtime.

```bash
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/agent.compose.yml up -d
```

## A2A agent

Run the agent only after supplying its MCP URL and model settings at runtime:

```bash
firefly-iii-agent --mcp-config mcp_config.json --web
```

Do not enable content-bearing telemetry by default. Validate configuration and trust
before launch with the doctor command documented on the configuration page.
