# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AgentTask(models.Model):
    _name = 'odoo.agent.task'
    _description = 'Agent Task'
    _order = 'create_date desc, id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', required=True, tracking=True)
    description = fields.Text(string='Description')
    agent_id = fields.Many2one(
        'odoo.agent',
        string='Agent',
        required=True,
        ondelete='cascade',
        index=True,
        tracking=True,
    )
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        ondelete='set null',
    )
    task_id = fields.Many2one(
        'project.task',
        string='Odoo Task',
        ondelete='set null',
        help='Link to an existing Odoo project task',
    )
    status = fields.Selection(
        [
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='pending',
        required=True,
        index=True,
        tracking=True,
    )
    result = fields.Text(string='Result/Output')
    error_message = fields.Text(string='Error Message')
    started_at = fields.Datetime(string='Started At')
    completed_at = fields.Datetime(string='Completed At')
    parent_id = fields.Many2one(
        'odoo.agent.task',
        string='Parent Task',
        ondelete='cascade',
        index=True,
    )
    child_ids = fields.One2many(
        'odoo.agent.task', 'parent_id', string='Subtasks',
    )
    log_ids = fields.One2many(
        'odoo.agent.log', 'agent_task_id', string='Execution Logs',
    )
    log_count = fields.Integer(
        string='Log Count',
        compute='_compute_log_count',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    @api.depends('log_ids')
    def _compute_log_count(self):
        for task in self:
            task.log_count = len(task.log_ids)

    @api.model
    def get_pending_tasks(self, agent_ids=None, limit=10):
        """Get pending tasks for polling by runtimes."""
        domain = [('status', '=', 'pending')]
        if agent_ids:
            domain.append(('agent_id', 'in', agent_ids))
        return self.search(domain, limit=limit)

    def action_start(self):
        self.ensure_one()
        self.write({
            'status': 'in_progress',
            'started_at': fields.Datetime.now(),
        })
        self._sync_project_task_stage()

    def action_complete(self, result=None):
        self.ensure_one()
        vals = {
            'status': 'completed',
            'completed_at': fields.Datetime.now(),
        }
        if result:
            vals['result'] = result
        self.write(vals)
        self._sync_project_task_stage()
        if self.task_id:
            self.task_id.message_post(
                body=f'Agent <b>{self.agent_id.name}</b> completed task: {self.name}',
                subject=f'Task completed: {self.name}',
            )

    def action_fail(self, error_message=None):
        self.ensure_one()
        vals = {
            'status': 'failed',
            'completed_at': fields.Datetime.now(),
        }
        if error_message:
            vals['error_message'] = error_message
        self.write(vals)
        self._sync_project_task_stage()
        if self.task_id:
            self.task_id.message_post(
                body=f'Agent <b>{self.agent_id.name}</b> failed task: {self.name}',
                subject=f'Task failed: {self.name}',
            )

    def _sync_project_task_stage(self):
        """Sync agent task status to linked project.task stage using configurable mapping."""
        self.ensure_one()
        if not self.task_id:
            return
        # Use configurable stage mapping
        stage = self.env['odoo.agent.stage.map'].get_stage_for_status(
            self.status, company_id=self.company_id.id
        )
        if stage:
            self.task_id.stage_id = stage.id
