# Public release checklist

Use this checklist before publishing the addon and runtime repositories.

## Repository hygiene

- [ ] No local absolute paths in public instructions.
- [ ] No secrets in tracked files.
- [ ] `.env` is ignored and `.env.example` is tracked.
- [ ] Local graph/cache folders are ignored.
- [ ] README explains value, install, runtime, security, and validation.
- [ ] License is declared.
- [ ] Version is updated in `__manifest__.py`.

## Odoo validation

- [ ] Install on a clean Odoo 18 database.
- [ ] Upgrade from a previously installed version.
- [ ] Run tests with `--test-enable`.
- [ ] Validate menus, actions, forms, kanban, and chatter.
- [ ] Validate non-admin Agent User permissions.
- [ ] Validate multi-company access if applicable.

## Runtime validation

- [ ] Linux manual run.
- [ ] Linux service install.
- [ ] macOS manual run.
- [ ] macOS launchd install.
- [ ] Windows manual run.
- [ ] Windows Scheduled Task install.
- [ ] Missing CLI reports failed execution.
- [ ] Runtime cancellation is acknowledged.

## End-to-end validation

- [ ] Create runtime in Odoo.
- [ ] Generate API key.
- [ ] Connect daemon.
- [ ] Create agent.
- [ ] Send Project task.
- [ ] Receive logs.
- [ ] Complete execution.
- [ ] Fail execution.
- [ ] Retry execution.
- [ ] Cancel execution.
- [ ] Delegate to another agent with `@mention`.

## Public demo

- [ ] Use demo data with no private customer names.
- [ ] Hide API keys and host secrets.
- [ ] Capture Project kanban with agent badges.
- [ ] Capture agent configuration tabs.
- [ ] Capture runtime online status.
- [ ] Capture execution logs and result.
- [ ] Capture `@mention` child execution.

## Publish

- [ ] Create public addon repository.
- [ ] Create public runtime repository.
- [ ] Push clean commits.
- [ ] Verify raw installer URLs.
- [ ] Create first release/tag.
- [ ] Publish LinkedIn post and demo material.
