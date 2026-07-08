# Compatibility

`odoo_agent` is an Odoo 18 addon. It integrates with the external Odoo Agent Runtime through the runtime API documented in [`runtime-contract.md`](runtime-contract.md).

## Version matrix

| Addon version | Runtime version | Status |
| --- | --- | --- |
| `18.0.1.4.x` | `>=0.1.0 <0.2.0` | First public baseline. |

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
