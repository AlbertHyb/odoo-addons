# Odoo Addons

Public Odoo 18 addon repository.

This repository contains installable Odoo addons intended to be consumed through a standard Odoo addons path, Git aggregator, submodule, deployment template, or any other Odoo-compatible source management flow.

## Available addons

| Addon | Summary | Documentation |
| --- | --- | --- |
| `odoo_agent` | AI agent execution system for Odoo Project: runtimes, agents, executions, logs, skills, MCP, and `@mentions`. | [`odoo_agent/README.md`](odoo_agent/README.md) |

## Repository strategy

This repository contains Odoo addons only.

Runtime daemons, OS installers, service files, and machine-side execution code live in a separate repository:

- Runtime: `https://github.com/nicolasramos/odoo-agent-runtime`

This separation keeps each project clean:

| Repository | Owns | Release rhythm |
| --- | --- | --- |
| `odoo-addons` | Odoo modules, manifests, XML views, models, security, Odoo tests, addon docs. | Odoo-versioned releases, for example `18.0.1.4.0`. |
| `odoo-agent-runtime` | Cross-platform daemon, installers, OS service integration, runtime docs, smoke tests. | Runtime semver releases, for example `0.1.0`. |

## Installation pattern

Add this repository to your Odoo addons path and install the desired module.

Example:

```ini
[options]
addons_path = /opt/odoo/odoo/addons,/opt/odoo/odoo-addons
```

Then install:

```bash
odoo-bin -d <database> -i odoo_agent --stop-after-init
```

## Documentation

- [`docs/repository-structure.md`](docs/repository-structure.md) — how this repository is organized.
- [`docs/release-policy.md`](docs/release-policy.md) — release and compatibility policy.
- [`odoo_agent/README.md`](odoo_agent/README.md) — addon product documentation.
- [`odoo_agent/docs/installation.md`](odoo_agent/docs/installation.md) — install the addon.
- [`odoo_agent/docs/runtime-installation.md`](odoo_agent/docs/runtime-installation.md) — connect the external runtime.

## Validate

```bash
python3 scripts/validate_addon.py
python3 -m compileall -q odoo_agent
```

Full validation requires Odoo 18:

```bash
odoo-bin -d <database> -i odoo_agent --test-enable --stop-after-init
```

## License

LGPL-3.
