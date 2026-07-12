# Odoo Addons

Public Odoo 18 addon repository.

This repository contains installable Odoo addons intended to be consumed through a standard Odoo addons path, Git aggregator, submodule, deployment template, or any other Odoo-compatible source management flow.


## Screenshots

<div align="center">
  <img src="odoo_agent/static/description/screenshots/Captura%20de%20pantalla%202026-07-12%20a%20las%2019.01.03.png" alt="Task with agent communication" width="700">
  <p><em>Task with agent communications, execution logs and agent chat</em></p>
</div>

<div align="center">
  <img src="odoo_agent/static/description/screenshots/Captura%20de%20pantalla%202026-07-12%20a%20las%2019.03.17.png" alt="Agent execution list" width="700">
  <p><em>Execution history with status, timestamps and log counts per run</em></p>
</div>

<div align="center">
  <img src="odoo_agent/static/description/screenshots/Captura%20de%20pantalla%202026-07-12%20a%20las%2019.04.02.png" alt="Runtime configuration" width="700">
  <p><em>Runtime detail with health status, version info, IP and heartbeat history</em></p>
</div>

<div align="center">
  <img src="odoo_agent/static/description/screenshots/Captura%20de%20pantalla%202026-07-12%20a%20las%2019.05.09.png" alt="Agent configuration form" width="700">
  <p><em>Agent setup: runtime, engine, CLI command, model, limits and instructions</em></p>
</div>

<div align="center">
  <img src="odoo_agent/static/description/screenshots/Captura%20de%20pantalla%202026-07-12%20a%20las%2019.08.40.png" alt="Agent chatter and status log" width="700">
  <p><em>Agent activity log: state changes, engine switches, working/idle/error cycles</em></p>
</div>


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


## Author

**Odoo AI Agent System (odoo_agent)** was created and is maintained by **Nicolás Ramos**
([nicolasramos.es](https://nicolasramos.es), [@nicolasramos_es](https://twitter.com/nicolasramos_es)).

This module is part of the Odoo ecosystem. If you find it useful, please contribute
via GitHub issues, pull requests, or by sharing your experience.

## License

LGPL-3.
