# Demo and launch script

This guide prepares screenshots and a short product video for a public launch.

## Core message

Do not present this as an AI chat.

Present it as an operational control layer for AI agents inside Odoo Project.

## Demo scenario

Project: `NovaForge Studio - Portal B2B Atlas`

Agents:

| Agent | Role | Mention key |
| --- | --- | --- |
| Hermes Dev N100 | Main implementation agent | `hermes` |
| QA Reviewer | Test and edge-case review | `qa` |
| Release Writer | Release notes and final summary | `release` |

Task:

```text
[NF-106] QA E2E del onboarding de nuevos tenants
```

Prompt:

```text
Prepare E2E test cases for tenant onboarding.
Include invitation, expired token, permission edge cases, and rollback checks.
Ask @qa to review missing edge cases.
```

## Screenshots

Capture at 1920×1080 or higher.

1. Project kanban with agent status badges.
2. Project task form with assigned agent and Send/Retry/Cancel actions.
3. Agent configuration with runtime, engine, CLI, instructions, skills, and MCP tabs.
4. Runtime form showing online/last seen/capabilities.
5. Execution form showing status, prompt, logs, result, and delegation.
6. Logs list showing streamed runtime output.
7. Chatter showing final result without raw HTML tags.
8. Child execution created by `@qa`.

## 90-second video outline

| Time | Scene | Voiceover |
| --- | --- | --- |
| 0–10s | Project kanban | “This is not another AI chat. This is Odoo operating agent work.” |
| 10–25s | Task form | “A Project task can be assigned to an agent and sent to an external runtime.” |
| 25–40s | Runtime | “The runtime can run on Linux, macOS, or Windows and executes local CLIs.” |
| 40–55s | Agent config | “Agents have engines, CLI commands, instructions, skills, MCP, timeouts, retries, and limits.” |
| 55–70s | Mention prompt | “Mention another agent with @qa and Odoo creates a traceable child execution.” |
| 70–85s | Logs/result | “Every run leaves status, logs, errors, result, and chatter history.” |
| 85–90s | Dashboard/kanban | “Odoo becomes the control layer for teams of agents.” |

## Capture rules

- Do not show API keys.
- Do not show private customer data.
- Use consistent demo names.
- Keep browser zoom readable.
- Prefer light UI for Odoo screenshots and premium dark frames for marketing slides.
- Verify no raw HTML tags appear in chatter, descriptions, or results.
