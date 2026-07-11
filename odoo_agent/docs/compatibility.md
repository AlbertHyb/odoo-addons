# Compatibility

`odoo_agent` is an Odoo 18 addon. It integrates with the external Odoo Agent Runtime through the runtime API documented in [`runtime-contract.md`](runtime-contract.md).

## Version matrix

| Addon version | Runtime version | Status |
| --- | --- | --- |
| `18.0.1.4.x` | `>=0.1.0 <0.2.0` | First public execution baseline. |
| `18.0.1.5.x` | `>=0.2.0 <0.3.0` | Chat executions and Odoo bus notifications. |
| `18.0.1.6.x` | `>=0.2.0 <0.3.0` | Task-context Agent Communications UI on top of chat executions. |
| `18.0.1.7.x` | `>=0.3.0 <0.4.0` | Public release. |

## Compatibility rules

- Addon releases follow Odoo-style versioning.
- Runtime releases follow semantic versioning.
- The runtime must support the execution API used by the addon.
- The addon keeps legacy task routes during the transition, but new integrations should use execution routes.

## Required runtime capabilities

The runtime should support:

- heartbeat;
- capabilities reporting;
- polling queued executions;
- start/log/complete/fail lifecycle calls;
- cancellation acknowledgement;
- CLI command placeholders;
- safe failure when a CLI is missing.
