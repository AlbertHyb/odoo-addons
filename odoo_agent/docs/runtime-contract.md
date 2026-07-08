# Runtime Contract

The Odoo addon and the external runtime communicate through a small JSON HTTP contract. The runtime is a separate process and should be treated as an untrusted integration client scoped by API key.

## Authentication

The runtime sends its API key through `X-API-Key` or `api_key`.

Odoo resolves the key to exactly one `odoo.agent.runtime`. Every execution/log operation must belong to that runtime.

## Poll response

`GET /api/agent/runtime/poll` returns queued executions:

```json
{
  "status": "ok",
  "executions": [
    {
      "id": 123,
      "name": "Task name",
      "prompt": "Full execution prompt",
      "timeout_seconds": 3600,
      "agent": {
        "engine": "opencode",
        "cli_command": "opencode run --instruction {instruction}",
        "instructions": "Agent rules",
        "skills": [],
        "mcp_servers": []
      }
    }
  ]
}
```

Legacy `tasks` remains only as compatibility fallback.

## Lifecycle endpoints

| Action | Endpoint |
| --- | --- |
| Start | `POST /api/agent/execution/{id}/start` |
| Log | `POST /api/agent/execution/{id}/log` |
| Complete | `POST /api/agent/execution/{id}/complete` |
| Fail | `POST /api/agent/execution/{id}/fail` |
| Request cancel | `POST /api/agent/execution/{id}/cancel` |
| Acknowledge cancel | `POST /api/agent/execution/{id}/cancel/ack` |
| Read logs | `GET /api/agent/execution/{id}/logs` |

## Runtime behavior expectations

- Use `prompt` as the primary execution input.
- Use `agent.cli_command` when present.
- Preserve long prompts as one CLI argument or pass them via an explicit file placeholder.
- If the configured CLI is missing, fail the execution.
- Never report fake success when the CLI was not executed.
- Stream useful logs back to Odoo while running.
