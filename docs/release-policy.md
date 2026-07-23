# Release policy

## Odoo addons

Odoo addons use Odoo-style versions in each `__manifest__.py`:

```text
17.0.<major>.<minor>.<patch>
```

Use this when the change depends on Odoo 17 APIs, Odoo data migrations, XML views, model fields, security, or addon behavior.

## Release checklist

Before publishing an addon release:

- [ ] Static validation passes.
- [ ] Odoo 17 install/upgrade passes.
- [ ] Odoo tests pass.
- [ ] README and docs are updated.
