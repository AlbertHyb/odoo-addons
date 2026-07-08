# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import html2plaintext


class ProjectTask(models.Model):
    _inherit = 'project.task'

    agent_id = fields.Many2one(
        'odoo.agent',
        string='AI Agent',
        ondelete='set null',
        tracking=True,
        check_company=True,
        help='Assign this task to an AI agent',
    )
    execution_ids = fields.One2many(
        'odoo.agent.execution',
        'task_id',
        string='Agent Executions',
    )
    latest_execution_id = fields.Many2one(
        'odoo.agent.execution',
        string='Latest Agent Execution',
        ondelete='set null',
        copy=False,
        check_company=True,
    )
    latest_execution_status = fields.Selection(
        related='latest_execution_id.status',
        string='Latest Agent Status',
        readonly=True,
    )
    execution_count = fields.Integer(
        string='Agent Execution Count',
        compute='_compute_execution_count',
    )
    agent_task_id = fields.Many2one(
        'odoo.agent.task',
        string='Legacy Agent Task',
        ondelete='set null',
        copy=False,
        help='Legacy tracking field. New flows use Agent Executions.',
    )
    agent_status = fields.Selection(
        related='latest_execution_id.status',
        string='Agent Status',
        readonly=True,
    )
    agent_chat_message_ids = fields.One2many(
        'odoo.agent.chat.message',
        'project_task_id',
        string='Agent Communications',
    )
    agent_chat_message_count = fields.Integer(
        string='Agent Communication Count',
        compute='_compute_agent_chat_message_count',
    )
    agent_chat_composer_agent_id = fields.Many2one(
        'odoo.agent',
        string='Message Agent',
        check_company=True,
        help='Agent that will receive the next task communication.',
    )
    agent_chat_composer_body = fields.Text(
        string='Message',
        help='Message to send to the selected agent in this task context.',
    )

    @api.depends('execution_ids')
    def _compute_execution_count(self):
        for task in self:
            task.execution_count = len(task.execution_ids)

    @api.depends('agent_chat_message_ids')
    def _compute_agent_chat_message_count(self):
        for task in self:
            task.agent_chat_message_count = len(task.agent_chat_message_ids)

    def _agent_execution_prompt(self):
        self.ensure_one()
        parts = [self.name or '']
        if self.description:
            parts.append(html2plaintext(self.description).strip())
        return '\n\n'.join(parts)

    def action_send_to_agent(self):
        for task in self:
            if not task.agent_id:
                raise UserError(_('Assign an AI agent before sending the task.'))
            if not task.agent_id.runtime_id:
                raise UserError(_('The selected AI agent must have a runtime.'))
            execution = self.env['odoo.agent.execution'].create({
                'name': task.name or _('Project Task'),
                'prompt': task._agent_execution_prompt(),
                'agent_id': task.agent_id.id,
                'runtime_id': task.agent_id.runtime_id.id,
                'project_id': task.project_id.id,
                'task_id': task.id,
                'requested_by_id': self.env.user.id,
                'company_id': task.company_id.id or self.env.company.id,
            })
            task.latest_execution_id = execution.id
        return True

    def action_assign_agent(self):
        return self.action_send_to_agent()

    def action_send_agent_chat_message(self):
        chat_model = self.env['odoo.agent.chat.message']
        for task in self:
            content = (task.agent_chat_composer_body or '').strip()
            agent = task.agent_chat_composer_agent_id or task.agent_id
            message, execution = chat_model.create_user_execution(
                agent,
                content,
                project_task=task,
                name=_('Chat message to %(agent)s') % {
                    'agent': agent.display_name if agent else _('Agent'),
                },
            )
            task.latest_execution_id = execution.id
            task.agent_chat_composer_body = False
            if not task.agent_chat_composer_agent_id:
                task.agent_chat_composer_agent_id = agent.id
            task.message_post(
                body=_('Agent communication queued for %s.') % agent.display_name,
                subject=_('Agent communication queued'),
            )
        return True

    def action_retry_agent_execution(self):
        self.ensure_one()
        if not self.latest_execution_id:
            return self.action_send_to_agent()
        execution = self.latest_execution_id.action_retry()
        self.latest_execution_id = execution.id
        return True

    def action_cancel_agent_execution(self):
        for task in self:
            if task.latest_execution_id:
                task.latest_execution_id.action_request_cancel()
        return True

    def action_view_agent_logs(self):
        self.ensure_one()
        execution_ids = self.execution_ids.ids
        return {
            'type': 'ir.actions.act_window',
            'name': _('Agent Logs'),
            'res_model': 'odoo.agent.log',
            'view_mode': 'list,form',
            'domain': [('execution_id', 'in', execution_ids)],
            'context': {'default_execution_id': self.latest_execution_id.id},
        }

    def action_view_agent_executions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Agent Executions'),
            'res_model': 'odoo.agent.execution',
            'view_mode': 'list,form',
            'domain': [('task_id', '=', self.id)],
            'context': {
                'default_task_id': self.id,
                'default_project_id': self.project_id.id,
                'default_agent_id': self.agent_id.id,
            },
        }

    def action_view_agent_communications(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Agent Communications'),
            'res_model': 'odoo.agent.chat.message',
            'view_mode': 'list,form',
            'domain': [('project_task_id', '=', self.id)],
            'context': {
                'default_project_task_id': self.id,
                'default_agent_id': self.agent_id.id,
            },
        }
