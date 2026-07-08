# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AgentChatMessage(models.Model):
    _name = 'odoo.agent.chat.message'
    _description = 'Agent Chat Message'
    _order = 'timestamp desc, id'
    _rec_name = 'content'
    _inherit = ['mail.thread']
    _check_company_auto = True

    agent_id = fields.Many2one(
        'odoo.agent',
        string='Agent',
        required=True,
        ondelete='cascade',
        index=True,
        check_company=True,
    )
    execution_id = fields.Many2one(
        'odoo.agent.execution',
        string='Execution',
        ondelete='set null',
        index=True,
        check_company=True,
    )
    author_id = fields.Many2one(
        'res.users',
        string='Author',
        required=True,
        default=lambda self: self.env.user,
    )
    author_type = fields.Selection(
        [
            ('user', 'User'),
            ('agent', 'Agent'),
        ],
        string='Author Type',
        default='user',
        required=True,
    )
    content = fields.Text(string='Message', required=True)
    task_id = fields.Many2one(
        'odoo.agent.task',
        string='Legacy Related Task',
        ondelete='set null',
    )
    project_task_id = fields.Many2one(
        'project.task',
        string='Related Project Task',
        ondelete='set null',
        check_company=True,
    )
    timestamp = fields.Datetime(
        string='Timestamp',
        required=True,
        default=fields.Datetime.now,
        index=True,
    )
    delivery_state = fields.Selection(
        [
            ('sent', 'Sent'),
            ('queued', 'Queued'),
            ('delivered', 'Delivered'),
            ('failed', 'Failed'),
        ],
        string='Delivery State',
        default='sent',
        required=True,
        index=True,
    )
    is_read = fields.Boolean(string='Is Read', default=False)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            agent = self.env['odoo.agent'].browse(vals.get('agent_id')) if vals.get('agent_id') else False
            execution = self.env['odoo.agent.execution'].browse(vals.get('execution_id')) if vals.get('execution_id') else False
            project_task = self.env['project.task'].browse(vals.get('project_task_id')) if vals.get('project_task_id') else False
            if execution:
                vals.setdefault('agent_id', execution.agent_id.id)
                vals.setdefault('project_task_id', execution.task_id.id)
                vals.setdefault('company_id', execution.company_id.id)
            elif project_task:
                vals.setdefault('company_id', project_task.company_id.id or self.env.company.id)
            elif agent:
                vals.setdefault('company_id', agent.company_id.id or self.env.company.id)
        messages = super().create(vals_list)
        for message in messages:
            message._notify_chat_event('chat_message_created')
        return messages

    def write(self, vals):
        result = super().write(vals)
        if {'content', 'delivery_state', 'is_read', 'execution_id'} & set(vals):
            for message in self:
                message._notify_chat_event('chat_message_updated')
        return result

    @api.model
    def send_user_message(self, agent_id, content, task_id=None, project_task_id=None, execution_id=None):
        """Send a message from a user to an agent."""
        return self.create({
            'agent_id': agent_id,
            'author_id': self.env.user.id,
            'author_type': 'user',
            'content': content,
            'task_id': task_id,
            'project_task_id': project_task_id,
            'execution_id': execution_id,
            'delivery_state': 'queued' if execution_id else 'sent',
        })

    @api.model
    def send_agent_message(self, agent_id, content, task_id=None, project_task_id=None, execution_id=None, author_id=None):
        """Send a message from an agent to a user."""
        return self.create({
            'agent_id': agent_id,
            'author_id': author_id or self.env.user.id,
            'author_type': 'agent',
            'content': content,
            'task_id': task_id,
            'project_task_id': project_task_id,
            'execution_id': execution_id,
            'delivery_state': 'delivered',
        })

    def mark_as_read(self):
        self.write({'is_read': True})

    @api.model
    def get_conversation(self, agent_id, project_task_id=None, limit=50):
        """Get chat history with an agent."""
        domain = [('agent_id', '=', agent_id)]
        if project_task_id:
            domain.append(('project_task_id', '=', project_task_id))
        return self.search(domain, limit=limit)

    def to_runtime_payload(self):
        self.ensure_one()
        return {
            'id': self.id,
            'author_type': self.author_type,
            'author_name': self.author_id.name,
            'content': self.content,
            'timestamp': fields.Datetime.to_string(self.timestamp) if self.timestamp else None,
            'delivery_state': self.delivery_state,
            'is_read': self.is_read,
            'execution_id': self.execution_id.id if self.execution_id else None,
            'project_task_id': self.project_task_id.id if self.project_task_id else None,
        }

    def _notify_chat_event(self, event_name):
        self.ensure_one()
        payload = {
            'event': event_name,
            'message': self.to_runtime_payload(),
            'agent_id': self.agent_id.id,
            'execution_id': self.execution_id.id if self.execution_id else None,
            'project_task_id': self.project_task_id.id if self.project_task_id else None,
        }
        self.env['bus.bus']._sendone(f'odoo_agent.agent.{self.agent_id.id}', 'odoo_agent', payload)
        if self.execution_id:
            self.env['bus.bus']._sendone(
                f'odoo_agent.execution.{self.execution_id.id}',
                'odoo_agent',
                payload,
            )
