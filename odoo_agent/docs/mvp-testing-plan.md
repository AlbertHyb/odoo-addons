# MVP Testing Plan

This document defines what is still missing before calling Odoo Agent System a stable public release, and what testers should validate directly in the testing environment.

Current verdict: the module is ready for **functional MVP / public alpha testing**. It is not yet a fully hardened production release.

## Quick path for testers

1. Upgrade the `odoo_agent` addon in an Odoo 18 testing database.
2. Start one connected runtime using the latest `odoo-agent-runtime` code.
3. Create one project with realistic tasks and at least two agents.
4. Run the critical test scenarios below.
5. Report each issue with screenshots, execution ID, runtime logs, and expected vs actual behavior.

## Release readiness levels

| Level | Meaning | Current status |
| --- | --- | --- |
| Prototype | Works in isolated demos but is not coherent enough for users. | Passed |
| Functional MVP / public alpha | Usable by technical testers with known gaps. | Current target |
| Public beta | Installable by external users with clear docs and repeatable setup. | Not yet |
| Stable release | Production-ready with security, upgrade, OS, and recovery validation. | Not yet |

## Critical validation checklist

These items decide whether the MVP is credible.

### 1. Odoo module install and upgrade

- [ ] Install `odoo_agent` from scratch in a clean Odoo 18 database.
- [ ] Upgrade an existing database that already has older `odoo_agent` data.
- [ ] Confirm no XML/view errors during module upgrade.
- [ ] Confirm backend assets load without missing SCSS/JS errors.
- [ ] Confirm translated languages install/load correctly: Spanish, Catalan/Valencian, Galician, Basque.

Acceptance criteria:

- Module installs and upgrades without traceback.
- Project task form opens correctly.
- Agent Communications tab renders correctly.
- Menus, actions, security groups, and views are accessible as expected.

### 2. Runtime connection and health

- [ ] Register a runtime in Odoo.
- [ ] Generate and copy the runtime API key.
- [ ] Start the runtime with Odoo URL and API key.
- [ ] Confirm heartbeat updates runtime status in Odoo.
- [ ] Confirm runtime capabilities are visible if reported.
- [ ] Confirm invalid API key is rejected.

Acceptance criteria:

- Runtime becomes visible as online/recently seen.
- Odoo only allows the runtime to operate its own executions.
- Missing or invalid API keys fail safely.

### 3. Project task execution flow

- [ ] Create a Project task with title and HTML description.
- [ ] Assign an agent.
- [ ] Click **Send to Agent**.
- [ ] Confirm execution becomes `queued`.
- [ ] Confirm runtime starts it and status becomes `running`.
- [ ] Confirm logs appear in Odoo.
- [ ] Confirm completion creates result and chatter audit entry.
- [ ] Confirm failed CLI creates `failed`, not fake success.

Acceptance criteria:

- Full task lifecycle works: queued → running → completed/failed.
- Logs are tied to the right execution and task.
- HTML from descriptions does not leak as raw tags into prompts or UI.

### 4. Agent Communications inside tasks

- [ ] Open a Project task and use **Agent Communications**.
- [ ] Send `Hola` or `Qué tal`.
- [ ] Confirm the agent answers conversationally, not by starting task work from the task title.
- [ ] Send a real follow-up instruction related to the task.
- [ ] Confirm runtime receives chat execution with `source=chat`.
- [ ] Confirm the final runtime result appears as an agent message in the thread.
- [ ] Confirm message order is chronological and readable.
- [ ] Confirm delivery states are visible and understandable.

Acceptance criteria:

- Short chat messages remain conversational.
- Task title is context, not the primary instruction for chat executions.
- Each chat message creates a traceable execution.
- The thread feels usable enough for daily task-agent communication.

### 5. Retry and cancellation

- [ ] Force a failed execution.
- [ ] Retry it from the task.
- [ ] Confirm a new execution attempt is created.
- [ ] Start a long-running execution.
- [ ] Request cancellation from Odoo.
- [ ] Confirm runtime acknowledges cancellation.
- [ ] Confirm final state becomes `cancelled`.

Acceptance criteria:

- Retry never overwrites historical execution evidence.
- Cancel is cooperative and auditable.
- UI status remains understandable during cancellation.

### 6. Multi-agent and mentions

- [ ] Configure at least two agents with mention handles.
- [ ] Send a task prompt containing `@qa` or another agent handle.
- [ ] Confirm a child execution is created for the mentioned agent.
- [ ] Confirm child execution links to the parent.
- [ ] Confirm child executions do not create infinite mention loops.

Acceptance criteria:

- Mentions create traceable delegated executions.
- Parent/child execution relationship is visible.
- Missing-runtime mentioned agents are skipped with clear audit feedback.

### 7. Skills and MCP configuration

- [ ] Create a skill and assign it to an agent.
- [ ] Configure an MCP server for an agent.
- [ ] Confirm runtime payload includes skills and MCP configuration.
- [ ] Confirm tips/help text is understandable in Odoo.
- [ ] Confirm secrets are not stored directly in unsafe places.

Acceptance criteria:

- Runtime receives enough configuration to execute without guessing from agent name.
- Admin users understand what each configuration area does.
- Sensitive values are handled according to docs/security guidance.

### 8. Security and permissions

- [ ] Test as Agent Admin.
- [ ] Test as Agent User.
- [ ] Test as regular Project user without agent groups.
- [ ] Test multi-company isolation.
- [ ] Confirm users cannot see or operate executions from inaccessible projects/tasks.
- [ ] Confirm runtime API key cannot access another runtime's executions.

Acceptance criteria:

- Permissions match Odoo project visibility and agent groups.
- Runtime API access is scoped to one runtime.
- No unnecessary `sudo()` exposure is visible from user testing.

### 9. Cross-platform runtime installation

Validate installers on real machines or VMs.

| OS | Required checks |
| --- | --- |
| Linux | interactive install, manual mode, systemd service, restart, uninstall/update notes |
| macOS | interactive install, manual/background mode, launch behavior, Python dependency setup |
| Windows | PowerShell install, manual/background mode, path handling, service/task scheduler decision |

Acceptance criteria:

- Non-expert users can follow installation prompts.
- Technical users can run the runtime manually for debugging.
- Empty API keys are rejected.
- Existing config is not overwritten silently.

### 10. Documentation and public release material

- [ ] README explains addon installation clearly.
- [ ] Runtime README explains Linux/macOS/Windows setup clearly.
- [ ] Runtime contract is accurate.
- [ ] Security guide is accurate.
- [ ] Demo script uses clean sample data.
- [ ] Screenshots do not show API keys, private URLs, or secrets.
- [ ] LinkedIn/post material points to the right repositories.

Acceptance criteria:

- A new tester can install and run the MVP from docs.
- Public docs do not overpromise unvalidated capabilities.
- Demo material shows a real workflow, not only configuration screens.

## Suggested testing data

Use consistent data so screenshots and bug reports are easier to compare.

| Object | Suggested value |
| --- | --- |
| Project | `OdooClaw` |
| Main task | `[NF-102] Implement Stripe → Odoo synchronizer` |
| Main agent | `OpenCode N100` |
| QA agent | `QA Agent` |
| Runtime | `N100 Runtime` |
| Skill | `Odoo Development` |
| MCP server | `GitHub MCP` or `Odoo MCP` |

Suggested task prompt:

```text
Review the current synchronization flow and propose the implementation plan for Stripe → Odoo.

Include:
- data model impact;
- webhook handling;
- idempotency;
- retry strategy;
- test cases.

Ask @qa to review edge cases.
```

Suggested chat checks:

```text
Hola
Qué tal?
Resume lo que has entendido antes de tocar nada.
Ahora céntrate solo en los webhooks.
```

## Bug report template

Use this format for testing issues.

```markdown
## Summary
Short description of the problem.

## Environment
- Odoo version:
- Addon commit/version:
- Runtime commit/version:
- OS:
- Browser:

## Steps
1.
2.
3.

## Expected
What should have happened.

## Actual
What happened instead.

## Evidence
- Screenshot:
- Execution ID:
- Runtime log snippet:
- Odoo traceback, if any:

## Severity
Critical / High / Medium / Low
```

## MVP exit criteria

The MVP can be presented publicly when all of these are true:

- [ ] One clean task execution E2E passes.
- [ ] One clean chat execution E2E passes.
- [ ] One failure case is visible and understandable.
- [ ] One retry case works.
- [ ] One cancellation case works.
- [ ] One mention/delegation case works.
- [ ] Runtime install works on at least Linux and macOS, with Windows documented or validated separately.
- [ ] A non-admin user test does not expose obvious permission leaks.
- [ ] Public docs are good enough for a technical external tester.
- [ ] Demo screenshots/video use non-sensitive data.

## Known follow-up development tasks

These are likely post-MVP or beta-hardening tasks.

| Area | Task | Priority |
| --- | --- | --- |
| Realtime UI | Add OWL subscriber/composer for live thread refresh without manual reload. | High |
| Runtime | Add long-prompt `{instruction_file}` placeholder support. | High |
| Runtime | Redact secrets from logged CLI commands. | High |
| Runtime | Validate Windows installer on a real Windows machine. | High |
| Odoo | Run full Odoo test suite with real DB install/upgrade. | High |
| Security | Deep review of record rules, project visibility, and runtime endpoints. | High |
| UX | Polish Agent Communications after browser screenshots from testing. | Medium |
| Ops | Add dashboard cards for blocked/failed/active executions. | Medium |
| Docs | Add troubleshooting examples from real tester failures. | Medium |
| Release | Prepare GitHub issues from this checklist. | Medium |

## Next step

Run the critical checklist in the testing environment and turn every failed item into a GitHub issue with the bug report template above.
