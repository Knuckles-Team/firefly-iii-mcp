---
name: firefly-iii-mcp-development
skill_type: skill
domain: development
description: >-
  Develop, test, gate, and release the firefly-iii-mcp connector. Use this skill
  when changing Firefly III API mappings, action-routed MCP tools, connector
  content, packaging, documentation, or repository gates.
license: MIT
tags: [firefly-iii, development, connector, test, gates]
tier: repository
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# firefly-iii-mcp development

This repository owns the Firefly III API client, action-routed MCP tools, and
connector content. Shared MCP contracts, transports, and source-ingest clients
belong to `scion-sdk`; admission, serving, and durable graph state
belong to their owning repositories. Read `AGENTS.md` before changing code and
keep provider credentials, customer data, private endpoints, and ledger values
out of source, logs, prompts, and packaged skill content.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver small, reviewable slices and cite the
owning spec row in the commit trailer.

- Find the owning row first with `git grep -n "<term>" -- specs` and extend the
  existing spec before adding new requirement text.
- Reuse the existing SDK HTTP client, resolved TLS profile, Firefly API mixins,
  and action-routed MCP modules. Do not create a second transport, graph-write
  path, or connector entry point.
- Bind every delivered requirement to a focused test. Generated `status.json`
  files are produced by `pipelines-hook spec-status`; never hand-edit them.
- Keep the connector boundary intact: Firefly III calls, mappings, and neutral
  source declarations live here, while shared MCP contracts, admission, and
  durable graph state live in their owning repositories.
- Put `Spec: <ID>` and the assisting agent trailer on consecutive final commit
  message lines.

## Setup and gates

Use the pinned environment and run the shared gates from the checkout root:

```bash
uv sync --locked
uvx pre-commit run --all-files
```

For focused feedback, use the tests that exercise the actual connector paths:

```bash
uv run --all-extras pytest tests/test_publication_workflow.py -q
uv run --all-extras pytest tests/test_startup.py tests/test_firefly_iii_mcp_validation.py -q
uv run --all-extras pytest tests/test_auth.py tests/test_api_wrapper.py -q
```

The external Firefly III API is never called by local tests. Keep credentials
out of fixtures. `FIREFLY_III_URL` and `FIREFLY_III_TOKEN` are runtime inputs;
`scion_sdk` owns their configuration, TLS, and delegation helpers.
Preserve HTTPS-only endpoints, resolved TLS profiles, OIDC delegation,
fixed-token redaction, and the condensed/verbose tool surfaces when changing the
client or tool modules.

## Packaging and publication

Keep `firefly_iii_mcp/skills/`, `firefly_iii_mcp/ontology/`, prompts, and
connector data in the package-data declaration. Build locally with `uv build`
and inspect wheel contents before release. The canonical Pages publisher is
`.github/workflows/pages.yml`, which calls the shared pipelines workflow with
`.config/spec-dashboard.json`; keep its `workflow_dispatch` path and do not add
another documentation publisher. The generated dashboard reads
`specs/*/status.json` and is published at `spec-delivery/`.

Before pushing, work in a real Git worktree based on `origin/main`, inspect the
complete diff, stage only reviewed paths, and verify `git status --short` after
each gate. Do not use `git stash`, `git add -A`, `git add .`, or force-push. Do
not claim Pages publication until a successful exact-source workflow run and the
public dashboard are both observed.
