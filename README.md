# Odoo AI Agent System

Public repository for the Odoo 18 AI Agent System addon.

The addon turns Odoo Project into an operational control layer for AI agents: assign agents to tasks, run work on external runtimes, stream logs, retry/cancel executions, configure skills and MCP servers, and delegate work with `@mentions`.

## Start here

- [`odoo_agent/README.md`](odoo_agent/README.md) — product overview and documentation index.
- [`odoo_agent/docs/installation.md`](odoo_agent/docs/installation.md) — addon installation.
- [`odoo_agent/docs/runtime-installation.md`](odoo_agent/docs/runtime-installation.md) — runtime installation overview.
- [`odoo_agent/docs/release-checklist.md`](odoo_agent/docs/release-checklist.md) — public release checklist.

## Validate

```bash
python3 scripts/validate_addon.py
python3 -m compileall -q odoo_agent
```

Full Odoo validation requires an Odoo 18 database:

```bash
odoo-bin -d <database> -i odoo_agent --test-enable --stop-after-init
```

## License

LGPL-3.
