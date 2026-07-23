# Odoo Addons

Public Odoo 17 addon repository.

This repository contains installable Odoo addons intended to be consumed through a standard Odoo addons path, Git aggregator, submodule, deployment template, or any other Odoo-compatible source management flow.

## Available addons

| Addon | Summary | Documentation |
| --- | --- | --- |
| `mail_bot_odooclaw` | OdooClaw AI bot integration with Odoo Discuss via webhooks. | [`mail_bot_odooclaw/README.md`](mail_bot_odooclaw/README.md) |

## Repository strategy

This repository contains Odoo addons only.

## Installation pattern

Add this repository to your Odoo addons path and install the desired module.

Example:

```ini
[options]
addons_path = /opt/odoo/odoo/addons,/opt/odoo/odoo-addons
```

Then install:

```bash
odoo-bin -d <database> -i mail_bot_odooclaw --stop-after-init
```

## Documentation

- [`docs/repository-structure.md`](docs/repository-structure.md) — how this repository is organized.
- [`docs/release-policy.md`](docs/release-policy.md) — release and compatibility policy.

## Validate

```bash
python3 -m compileall -q mail_bot_odooclaw
```

Full validation requires Odoo 17:

```bash
odoo-bin -d <database> -i mail_bot_odooclaw --test-enable --stop-after-init
```

## Author

**Mail Bot OdooClaw** was created and is maintained by **Nicolás Ramos**
([nicolasramos.es](https://nicolasramos.es), [@nicolasramos_es](https://twitter.com/nicolasramos_es)).

This module is part of the Odoo ecosystem. If you find it useful, please contribute
via GitHub issues, pull requests, or by sharing your experience.

## License

AGPL-3.
