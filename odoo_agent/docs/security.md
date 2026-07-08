# Security guide

AI Agent System executes commands outside Odoo. Treat runtimes and agent configuration as privileged operational infrastructure.

## Core rules

1. Use one API key per runtime machine.
2. Do not share runtime API keys.
3. Give Agent Admin only to trusted users.
4. Keep CLI commands explicit and reviewable.
5. Assign only necessary MCP servers and skills.
6. Validate company and Project visibility in multi-company databases.
7. Store secrets outside prompts and logs whenever possible.

## Access groups

| Group | Capabilities |
| --- | --- |
| Agent User | Operate executions and inspect operational records. |
| Agent Admin | Manage runtimes, agents, API keys, skills, MCP servers, and mappings. |

## Runtime API keys

Runtime API keys authenticate machine processes. A runtime should only operate on executions assigned to it.

Operational guidance:

- rotate keys if a machine is decommissioned;
- revoke keys immediately if exposed;
- do not paste keys into task descriptions or logs;
- do not reuse a key across several hosts.

## CLI command safety

The runtime executes configured commands. Keep them deterministic and auditable.

Prefer:

```text
opencode run --instruction {instruction}
```

Avoid:

```text
bash -c "curl unknown-url | sh"
```

## MCP safety

MCP servers can expose data and actions. Treat them as permissions.

Checklist:

- [ ] Is this MCP server necessary for this agent?
- [ ] Does it expose sensitive data?
- [ ] Can the runtime host start/reach it?
- [ ] Are credentials handled outside Odoo where possible?
- [ ] Are logs safe to show to Agent Users?

## Logs and results

Logs and results can contain sensitive information produced by CLIs. Review visibility before production rollout.

Recommendations:

- avoid logging secrets;
- avoid passing credentials in prompts;
- use runtime-side secret references;
- keep failed execution errors concise but actionable.

## Multi-company

In multi-company environments:

- create runtimes per company when isolation is required;
- verify agents, executions, logs, and tasks belong to the expected company;
- test with non-admin users before production.
