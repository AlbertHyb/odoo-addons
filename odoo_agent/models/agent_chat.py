# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AgentChatMessage(models.Model):
    _name = 'odoo.agent.chat.message'
    _description = 'Agent Chat Message'
    _order = 'timestamp desc, id'
    _rec_name = 'content'
    _inherit = ['mail.thread']

    agent_id = fields.Many2one(
        'odoo.agent',
        string='Agent',
        required=True,
        ondelete='cascade',
        index=True,
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
        string='Related Task',
        ondelete='set null',
    )
    timestamp = fields.Datetime(
        string='Timestamp',
        required=True,
        default=fields.Datetime.now,
        index=True,
    )
    is_read = fields.Boolean(string='Is Read', default=False)

    @api.model
    def send_user_message(self, agent_id, content, task_id=None):
        """Send a message from a user to an agent."""
        return self.create({
            'agent_id': agent_id,
            'author_id': self.env.user.id,
            'author_type': 'user',
            'content': content,
            'task_id': task_id,
        })

    @api.model
    def send_agent_message(self, agent_id, content, task_id=None):
        """Send a message from an agent to a user."""
        return self.create({
            'agent_id': agent_id,
            'author_id': self.env.user.id,
            'author_type': 'agent',
            'content': content,
            'task_id': task_id,
        })

    def mark_as_read(self):
        self.write({'is_read': True})

    @api.model
    def get_conversation(self, agent_id, limit=50):
        """Get chat history with an agent."""
        return self.search([
            ('agent_id', '=', agent_id),
        ], limit=limit)
