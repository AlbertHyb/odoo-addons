# Configuration guide

This guide explains how to configure runtimes, agents, skills, MCP servers, and execution limits.

## Configuration model

| Object | Role |
| --- | --- |
| Runtime | A machine/process that polls Odoo and runs local CLIs. |
| Agent | Business-facing worker configuration. |
| Skill | Reusable instruction pack injected into executions. |
| MCP Server | Tool/data-source configuration sent to the runtime. |
| Execution | One auditable run against a Project task. |

## Runtime configuration

Create one runtime per executing machine.

Recommended fields:

| Field | Recommendation |
| --- | --- |
| Name | Use a machine-readable name, for example `agent-worker-01`. |
| API key | Generate per runtime. Never share between hosts. |
| Company | Set when using multi-company databases. |
| Capabilities | Let the runtime report installed tools when possible. |

## Agent configuration

| Field | Purpose |
| --- | --- |
| Name | Human-readable agent name. |
| Mention key | Short handle for `@mentions`, for example `qa`. |
| Runtime | Machine that will run this agent. |
| Engine | Preset category: Codex, Hermes, OpenCode, OpenClaw, Claude Code, or Custom CLI. |
| CLI Command | Exact command executed by the runtime. |
| Instructions | Stable operating rules for the agent. |
| Skills | Reusable capability packs. |
| MCP Servers | Tool/data access available during execution. |
| Timeout | Maximum runtime duration. |
| Retry limit | Maximum automatic/manual retry policy. |
| Concurrency | Maximum active executions for that agent. |

## CLI command examples

```text
opencode run {instruction}
hermes run --context {instruction}
openclaw agent --task {task_name} --context {instruction}
claude --print {instruction}
python -m internal_agent --task {task_id} --prompt {instruction}
```

Use explicit placeholders. Avoid commands that depend on shell-specific quoting.

## Skills

Use skills for reusable capabilities, not whole personalities.

Good skill examples:

- `QA test case writer`
- `Odoo migration reviewer`
- `Security checklist auditor`
- `Release note writer`

Bad skill examples:

- `Do everything`
- `Be smart`
- `General developer`

Each skill should explain:

- when to use it;
- required inputs;
- expected output;
- guardrails;
- what not to do.

## MCP servers

MCP server configuration tells the runtime which external tools or data sources can be used.

Recommendations:

- assign only trusted MCP servers;
- avoid broad access by default;
- keep credentials outside Odoo when possible;
- document what each server exposes;
- validate the runtime host can actually start or reach the server.

## Execution limits

Start conservative:

| Limit | Suggested first value |
| --- | --- |
| Timeout | 900 seconds |
| Retry limit | 1 |
| Concurrency | 1 or 2 |

Increase only after observing runtime load and failure modes.

## Multi-agent delegation

Set a short mention key for agents that should be callable from prompts.

Example:

| Agent | Mention key |
| --- | --- |
| QA Reviewer | `qa` |
| Security Auditor | `security` |
| Release Writer | `release` |

Prompt:

```text
Implement the onboarding checklist and ask @qa to review the acceptance cases.
```

Odoo creates a child execution for `@qa` and links it to the parent execution.
