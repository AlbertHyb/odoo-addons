# Translations

The addon ships with a gettext template and starter translations for the main languages used in Spain.

## Included files

| File | Language |
| --- | --- |
| `i18n/odoo_agent.pot` | Translation template |
| `i18n/es.po` | Spanish |
| `i18n/ca.po` | Catalan / Valencian |
| `i18n/ca_ES.po` | Catalan / Valencian regional variant |
| `i18n/gl.po` | Galician |
| `i18n/eu.po` | Basque |

## Regenerate translations

From the repository root:

```bash
# generate_i18n.py was removed in cleanup; regenerate manually if needed
python3 .github/scripts/validate_addon.py
```

The generator extracts common Odoo UI strings from Python, XML, and the addon manifest. It also reuses local Odoo base translations when available and applies module-specific translations for the agent execution terminology.

## Review policy

These translations are a public baseline. Native speaker review is welcome, especially for technical terms such as runtime, prompt, skill, execution, and MCP.

When improving translations:

- keep placeholders such as `%s` and `%(agent)s` unchanged;
- keep HTML tags in translated strings when the source string has them;
- do not translate technical model names such as `project.task`;
- run validation before committing.

## Valencian note

Odoo 18 includes Catalan translations through `ca.po`. This repository also includes `ca_ES.po` as a regional variant so deployments that use a separate Catalan/Valencian language code can still load the same baseline.
