# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    agent_id = fields.Many2one(
        'odoo.agent',
        string='AI Agent',
        ondelete='set null',
        tracking=True,
        help='Assign this task to an AI agent',
    )
    agent_task_id = fields.Many2one(
        'odoo.agent.task',
        string='Agent Task',
        ondelete='set null',
        copy=False,
        help='Linked agent task for tracking execution',
    )
    agent_status = fields.Selection(
        related='agent_task_id.status',
        string='Agent Status',
        readonly=True,
    )

    def action_assign_agent(self):
        """Assign this task to the selected agent."""
        self.ensure_one()
        if not self.agent_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Assign AI Agent',
                'res_model': 'odoo.agent',
                'view_mode': 'form',
                'target': 'new',
            }
        # Create agent task
        agent_task = self.env['odoo.agent.task'].create({
            'name': self.name,
            'description': self.description or '',
            'agent_id': self.agent_id.id,
            'project_id': self.project_id.id,
            'task_id': self.id,
        })
        self.agent_task_id = agent_task.id
        self.message_post(
            body=f'Task assigned to AI agent: <b>{self.agent_id.name}</b>',
            subject='Task assigned to AI agent',
        )
        return True
