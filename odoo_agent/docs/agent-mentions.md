# Agent Mentions and Delegation

Agent mentions let one execution create traceable child executions for other agents by using `@handle` in the prompt.

## Quick path

1. Configure each agent with a **Mention Handle** such as `qa`, `devops`, or `hermes`.
2. Write a task or execution prompt that includes the mention, for example:

   ```text
   Implement the onboarding flow and ask @qa to review edge cases.
   ```

3. Send the task to the primary agent.
4. Odoo creates the parent execution and one child execution for each mentioned agent with a runtime.
5. Review child executions from the execution's **Delegations** tab.

## Rules

| Rule | Behavior |
| --- | --- |
| Mention syntax | `@handle`, using letters, numbers, dots, underscores, or hyphens. |
| Resolution | Odoo matches `mention_key` first, then a normalized version of the agent name. |
| Scope | Mentions are resolved inside the execution company. |
| Loop prevention | Child executions do not create more child executions automatically. |
| Missing runtime | Mentioned agents without runtime are skipped and noted in chatter. |
| Same agent | Mentioning the current agent is ignored to avoid duplicate work. |

## Why this matters

This creates a practical multi-agent workflow without losing Odoo traceability:

- Project task remains the business object.
- Parent execution shows who started the work.
- Child executions show which agents were called in.
- Logs/results stay separated per agent.
- Chatter records delegation events.
