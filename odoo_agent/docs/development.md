# Development guide

This guide defines the maintainable development baseline for the Odoo AI Agent System addon.

## Quick path

1. Make changes inside `odoo_agent/`.
2. Run static validation:

   ```bash
   python3 scripts/validate_addon.py
   python3 -m compileall -q odoo_agent
   ```

3. Run Odoo tests in a real Odoo 18 database before shipping:

   ```bash
   odoo-bin -d <database> -i odoo_agent --test-enable --stop-after-init
   ```

## Code layout

| Path | Purpose |
| --- | --- |
| `odoo_agent/models/` | Odoo models for agents, runtimes, executions, logs, skills, MCP, and Project integration. |
| `odoo_agent/controllers/` | Runtime and chat API endpoints. |
| `odoo_agent/views/` | Menus, forms, lists, kanban/search extensions, and operational screens. |
| `odoo_agent/security/` | Groups, access control, and record rules. |
| `odoo_agent/tests/` | Odoo TransactionCase and controller tests. |
| `odoo_agent/docs/` | Public documentation. |
| `scripts/` | Repository validation helpers. |

## Test areas

| Area | Required coverage |
| --- | --- |
| Models | Agent, runtime, execution, logs, skills, MCP, retry, cancel, chatter safety. |
| Controllers | API key auth, JSON payloads, invalid payloads, runtime ownership, cross-runtime denial. |
| Project workflow | Assign agent, send to runtime, start, log, complete, fail, retry, cancel. |
| Security | Groups, API keys, multi-company isolation, project/task visibility. |
| Runtime compatibility | Legacy task routes and first-class execution routes. |

## Development rules

- Keep the Odoo addon and runtime as separate concerns.
- Do not bypass record rules with `sudo()` unless a controller has already authenticated and scoped the runtime/user.
- Every runtime endpoint must validate ownership before reading or mutating executions/logs.
- Every user-facing configuration tab should explain why it exists and how to use it.
- Store prompts/results/logs safely; never render unescaped dynamic HTML in chatter.
- Convert Odoo HTML descriptions to plaintext before sending them to runtime prompts.
- Generated technical artifacts stay in English unless explicitly requested otherwise.

## Static validation

`scripts/validate_addon.py` checks:

- Python syntax through `ast`.
- XML parseability.
- `ir.model.access.csv` structure and permission values.
- Absence of forbidden external branding in addon files.

These checks do not replace Odoo database tests. They only catch fast local mistakes.

## Versioning

Use Odoo-style versions in `__manifest__.py`:

```text
18.0.<major>.<minor>.<patch>
```

Increment before public releases or meaningful upgrade steps.

## Commit style

Use conventional commits:

```text
feat: add execution retry flow
fix: clean task html descriptions
chore: add runtime installation docs
```

Do not include AI attribution trailers.
