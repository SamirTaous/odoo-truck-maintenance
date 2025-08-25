from odoo import models, fields, api, _
from datetime import datetime, timedelta

class TruckMaintenanceRequest(models.Model):
    _name = 'truck.maintenance.request'
    _description = 'Truck Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, request_date desc'
    
    name = fields.Char('Request Subject', required=True, tracking=True)
    description = fields.Text('Description')
    request_date = fields.Date('Request Date', default=fields.Date.context_today, tracking=True)
    truck_id = fields.Many2one('truck.vehicle', string='Truck', required=True, tracking=True)
    maintenance_type = fields.Selection([
        ('preventive', 'Preventive'),
        ('corrective', 'Corrective'),
        ('inspection', 'Inspection'),
        ('emergency', 'Emergency')
    ], string='Maintenance Type', default='corrective', required=True, tracking=True)
    
    priority = fields.Selection([
        ('0', 'Very Low'),
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High'),
        ('4', 'Very High')
    ], string='Priority', default='2', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    # Maintenance details
    maintenance_team_id = fields.Many2one('truck.maintenance.team', string='Maintenance Team')
    technician_id = fields.Many2one('res.users', string='Assigned Technician', tracking=True)
    scheduled_date = fields.Datetime('Scheduled Date', tracking=True)
    completion_date = fields.Datetime('Completion Date', tracking=True)
    
    # Cost tracking
    estimated_cost = fields.Float('Estimated Cost', tracking=True)
    actual_cost = fields.Float('Actual Cost', tracking=True)
    
    # Parts and labor
    parts_needed = fields.Text('Parts Needed')
    labor_hours = fields.Float('Labor Hours')
    
    # Maintenance category
    category = fields.Selection([
        ('engine', 'Engine'),
        ('transmission', 'Transmission'),
        ('brakes', 'Brakes'),
        ('tires', 'Tires'),
        ('electrical', 'Electrical'),
        ('hydraulic', 'Hydraulic'),
        ('body', 'Body Work'),
        ('other', 'Other')
    ], string='Category', tracking=True)
    
    # Odometer reading
    odometer_reading = fields.Float('Odometer Reading (km)', help='Current odometer reading when maintenance is requested')
    
    # Notes and resolution
    work_performed = fields.Text('Work Performed')
    notes = fields.Text('Additional Notes')
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('truck.maintenance.request') or _('New')
        return super().create(vals)
    
    def action_request(self):
        self.state = 'requested'
    
    def action_start(self):
        self.state = 'in_progress'
        if not self.scheduled_date:
            self.scheduled_date = fields.Datetime.now()
    
    def action_done(self):
        self.state = 'done'
        self.completion_date = fields.Datetime.now()
    
    def action_cancel(self):
        self.state = 'cancelled'
    
    def action_reset_to_draft(self):
        self.state = 'draft'


class TruckMaintenanceTeam(models.Model):
    _name = 'truck.maintenance.team'
    _description = 'Truck Maintenance Team'
    
    name = fields.Char('Team Name', required=True)
    member_ids = fields.Many2many('res.users', string='Team Members')
    leader_id = fields.Many2one('res.users', string='Team Leader')
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Color Index', default=0)