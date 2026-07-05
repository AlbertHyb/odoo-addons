# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Agent(models.Model):
    _name = 'odoo.agent'
    _description = 'AI Agent'
    _order = 'name, id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, index=True, tracking=True)
    description = fields.Text(string='Description')
    instructions = fields.Text(
        string='Instructions',
        help='System prompt / instructions for the agent',
    )
    runtime_id = fields.Many2one(
        'odoo.agent.runtime',
        string='Runtime',
        ondelete='set null',
        tracking=True,
    )
    model = fields.Char(string='Model', help='LLM model to use')
    status = fields.Selection(
        [
            ('idle', 'Idle'),
            ('working', 'Working'),
            ('error', 'Error'),
        ],
        string='Status',
        default='idle',
        required=True,
        index=True,
        tracking=True,
    )
    avatar = fields.Binary(string='Avatar')
    skill_ids = fields.Many2many(
        'odoo.agent.skill',
        'agent_skill_rel',
        'agent_id',
        'skill_id',
        string='Skills',
    )
    max_concurrent_tasks = fields.Integer(
        string='Max Concurrent Tasks',
        default=1,
        required=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Linked User',
        help='Optional: link to an Odoo user for permissions',
    )
    task_ids = fields.One2many(
        'odoo.agent.task', 'agent_id', string='Tasks',
    )
    active_task_count = fields.Integer(
        string='Active Tasks',
        compute='_compute_active_task_count',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(string='Active', default=True)

    @api.depends('task_ids', 'task_ids.status')
    def _compute_active_task_count(self):
        for agent in self:
            agent.active_task_count = len(
                agent.task_ids.filtered(
                    lambda t: t.status in ('pending', 'in_progress')
                )
            )

    def action_assign_runtime(self):
        """Open runtime selection wizard."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assign Runtime',
            'res_model': 'odoo.agent.runtime',
            'view_mode': 'form',
            'target': 'new',
        }
