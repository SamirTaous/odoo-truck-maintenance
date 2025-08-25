from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TruckVehicle(models.Model):
    _name = 'truck.vehicle'
    _description = 'Truck Vehicle'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Truck ID', required=True, copy=False, readonly=True, default='New')
    active = fields.Boolean(default=True, tracking=True)
    image = fields.Image(string="Truck Image")
    
    # Basic Truck Information
    license_plate = fields.Char(string='License Plate', required=True, tracking=True)
    vin_number = fields.Char(string='VIN Number', help='Vehicle Identification Number')
    year = fields.Integer(string='Year', required=True)
    
    # Truck Brand and Model (Major truck manufacturers)
    brand = fields.Selection([
        ('volvo', 'Volvo'),
        ('scania', 'Scania'),
        ('mercedes', 'Mercedes-Benz'),
        ('man', 'MAN'),
        ('iveco', 'Iveco'),
        ('daf', 'DAF'),
        ('renault', 'Renault Trucks'),
        ('mack', 'Mack'),
        ('peterbilt', 'Peterbilt'),
        ('kenworth', 'Kenworth'),
        ('freightliner', 'Freightliner'),
        ('international', 'International'),
        ('isuzu', 'Isuzu'),
        ('hino', 'Hino'),
        ('fuso', 'Fuso'),
        ('other', 'Other')
    ], string='Brand', required=True, tracking=True)
    
    model_name = fields.Char(string='Model', required=True)
    
    # Ownership and Availability
    ownership_type = fields.Selection([
        ('owned', 'Company Owned'),
        ('rented', 'Rented'),
        ('subcontracted', 'Subcontracted')  # This is the term for borrowed/temporary trucks
    ], string='Ownership Type', required=True, default='owned', tracking=True)
    
    rental_start_date = fields.Date(string='Rental Start Date')
    rental_end_date = fields.Date(string='Rental End Date')
    rental_cost_per_day = fields.Monetary(string='Daily Rental Cost', currency_field='currency_id')
    subcontractor_id = fields.Many2one('res.partner', string='Subcontractor', 
                                     domain=[('is_company', '=', True)])
    
    # Driver Information
    driver_id = fields.Many2one('res.partner', string='Assigned Driver', 
                               domain=[('is_company', '=', False)], tracking=True)
    
    # Truck Specifications for Freight
    truck_type = fields.Selection([
        ('rigid', 'Rigid Truck'),
        ('articulated', 'Articulated (Tractor-Trailer)'),
        ('b_double', 'B-Double'),
        ('road_train', 'Road Train')
    ], string='Truck Type', required=True, default='rigid')
    
    # Cargo Capacity
    max_payload = fields.Float(string='Max Payload (kg)', required=True, 
                              help='Maximum weight capacity in kilograms')
    cargo_volume = fields.Float(string='Cargo Volume (m³)', required=True,
                               help='Maximum cargo volume in cubic meters')
    cargo_length = fields.Float(string='Cargo Length (m)', help='Cargo area length in meters')
    cargo_width = fields.Float(string='Cargo Width (m)', help='Cargo area width in meters')
    cargo_height = fields.Float(string='Cargo Height (m)', help='Cargo area height in meters')
    
    # Truck Dimensions
    overall_length = fields.Float(string='Overall Length (m)')
    overall_width = fields.Float(string='Overall Width (m)')
    overall_height = fields.Float(string='Overall Height (m)')
    gross_vehicle_weight = fields.Float(string='GVW (kg)', help='Gross Vehicle Weight in kg')
    
    # Engine and Performance
    engine_power = fields.Integer(string='Engine Power (HP)')
    fuel_type = fields.Selection([
        ('diesel', 'Diesel'),
        ('petrol', 'Petrol'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('lng', 'LNG (Liquefied Natural Gas)'),
        ('cng', 'CNG (Compressed Natural Gas)')
    ], string='Fuel Type', default='diesel')
    fuel_capacity = fields.Float(string='Fuel Tank Capacity (L)')
    fuel_consumption = fields.Float(string='Fuel Consumption (L/100km)')
    
    # Special Equipment
    has_crane = fields.Boolean(string='Has Crane')
    has_tailgate = fields.Boolean(string='Has Tailgate Lift')
    has_refrigeration = fields.Boolean(string='Refrigerated')
    has_gps = fields.Boolean(string='GPS Tracking', default=True)
    special_equipment = fields.Text(string='Special Equipment')
    
    # Compliance and Documentation
    registration_expiry = fields.Date(string='Registration Expiry', tracking=True)
    insurance_expiry = fields.Date(string='Insurance Expiry', tracking=True)
    inspection_due = fields.Date(string='Next Inspection Due', tracking=True)
    
    # Maintenance Fields
    maintenance_request_ids = fields.One2many('maintenance.request', 'equipment_id', string='Maintenance Requests')
    maintenance_count = fields.Integer(string="Maintenance Count", compute='_compute_maintenance_count')
    last_maintenance_date = fields.Date(string='Last Maintenance', compute='_compute_last_maintenance')
    next_maintenance_due = fields.Date(string='Next Maintenance Due')
    maintenance_status = fields.Selection([
        ('good', 'Good'),
        ('needs_attention', 'Needs Attention'),
        ('critical', 'Critical')
    ], string='Maintenance Status', default='good', tracking=True)
    
    # Mileage and Usage
    odometer = fields.Float(string='Odometer (km)', help='Current odometer reading')
    last_service_odometer = fields.Float(string='Last Service Odometer (km)')
    service_interval_km = fields.Float(string='Service Interval (km)', default=10000)
    
    # Financial
    currency_id = fields.Many2one('res.currency', string='Currency', 
                                 default=lambda self: self._get_mad_currency())
    purchase_price = fields.Monetary(string='Purchase Price', currency_field='currency_id')
    current_value = fields.Monetary(string='Current Value', currency_field='currency_id')
    
    # Relations
    company_id = fields.Many2one('res.company', string='Company', 
                                default=lambda self: self.env.company)
    
    # Computed Fields
    is_available = fields.Boolean(string='Available', compute='_compute_availability', store=True)
    rental_status = fields.Char(string='Rental Status', compute='_compute_rental_status')
    km_until_service = fields.Float(string='KM Until Service', compute='_compute_service_due')
    
    @api.depends('maintenance_request_ids')
    def _compute_maintenance_count(self):
        for truck in self:
            truck.maintenance_count = len(truck.maintenance_request_ids)
    
    @api.depends('maintenance_request_ids.request_date')
    def _compute_last_maintenance(self):
        for truck in self:
            completed_maintenance = truck.maintenance_request_ids.filtered(
                lambda r: r.stage_id.done and r.request_date
            ).sorted('request_date', reverse=True)
            truck.last_maintenance_date = completed_maintenance[0].request_date if completed_maintenance else False
    
    @api.depends('odometer', 'last_service_odometer', 'service_interval_km')
    def _compute_service_due(self):
        for truck in self:
            if truck.odometer and truck.last_service_odometer and truck.service_interval_km:
                km_since_service = truck.odometer - truck.last_service_odometer
                truck.km_until_service = truck.service_interval_km - km_since_service
            else:
                truck.km_until_service = 0
    
    @api.depends('ownership_type', 'rental_end_date', 'active', 'maintenance_status')
    def _compute_availability(self):
        today = fields.Date.today()
        for truck in self:
            if not truck.active or truck.maintenance_status == 'critical':
                truck.is_available = False
            elif truck.ownership_type == 'rented' and truck.rental_end_date:
                truck.is_available = truck.rental_end_date >= today
            else:
                truck.is_available = True
    
    @api.depends('ownership_type', 'rental_start_date', 'rental_end_date')
    def _compute_rental_status(self):
        today = fields.Date.today()
        for truck in self:
            if truck.ownership_type == 'owned':
                truck.rental_status = 'Company Owned'
            elif truck.ownership_type == 'subcontracted':
                truck.rental_status = 'Subcontracted'
            elif truck.ownership_type == 'rented':
                if not truck.rental_start_date or not truck.rental_end_date:
                    truck.rental_status = 'Rental - Dates Missing'
                elif today < truck.rental_start_date:
                    truck.rental_status = 'Rental - Future'
                elif today > truck.rental_end_date:
                    truck.rental_status = 'Rental - Expired'
                else:
                    days_left = (truck.rental_end_date - today).days
                    truck.rental_status = f'Rental - {days_left} days left'
            else:
                truck.rental_status = 'Unknown'

    @api.constrains('rental_start_date', 'rental_end_date', 'ownership_type')
    def _check_rental_dates(self):
        for truck in self:
            if truck.ownership_type == 'rented':
                if truck.rental_start_date and truck.rental_end_date:
                    if truck.rental_start_date >= truck.rental_end_date:
                        raise ValidationError("Rental end date must be after start date.")
    
    @api.constrains('max_payload', 'cargo_volume')
    def _check_capacity_values(self):
        for truck in self:
            if truck.max_payload and truck.max_payload <= 0:
                raise ValidationError("Maximum payload must be greater than 0.")
            if truck.cargo_volume and truck.cargo_volume <= 0:
                raise ValidationError("Cargo volume must be greater than 0.")
    
    @api.onchange('cargo_length', 'cargo_width', 'cargo_height')
    def _onchange_cargo_dimensions(self):
        if self.cargo_length and self.cargo_width and self.cargo_height:
            self.cargo_volume = self.cargo_length * self.cargo_width * self.cargo_height
    
    def write(self, vals):
        # Validate ownership-specific requirements on save
        result = super().write(vals)
        for truck in self:
            if truck.ownership_type == 'rented':
                if not truck.rental_start_date or not truck.rental_end_date:
                    raise ValidationError("Rental start date and end date are required for rented trucks.")
            elif truck.ownership_type == 'subcontracted':
                if not truck.subcontractor_id:
                    raise ValidationError("Subcontractor company is required for subcontracted trucks.")
        return result
    
    @api.model_create_multi
    def create(self, vals_list):
        # Set sequence and validate ownership-specific requirements
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('truck.vehicle.sequence') or 'New'
            
            # Validate ownership-specific requirements
            if vals.get('ownership_type') == 'rented':
                if not vals.get('rental_start_date') or not vals.get('rental_end_date'):
                    raise ValidationError("Rental start date and end date are required for rented trucks.")
            elif vals.get('ownership_type') == 'subcontracted':
                if not vals.get('subcontractor_id'):
                    raise ValidationError("Subcontractor company is required for subcontracted trucks.")
        
        return super().create(vals_list)
        
    def action_view_maintenance(self):
        return {
            'name': 'Truck Maintenance',
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.request',
            'view_mode': 'kanban,tree,form',
            'domain': [('equipment_id', '=', self.id)],
            'context': {'default_equipment_id': self.id, 'default_name': f'Maintenance for {self.name}'}
        }
    
    def action_schedule_maintenance(self):
        """Action to schedule maintenance for the truck"""
        return {
            'name': 'Schedule Maintenance',
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.request',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': f'Maintenance for {self.name}',
                'default_equipment_id': self.id,
            }
        }
    
    def action_confirm_truck(self):
        """Confirm and activate the truck"""
        self.write({'active': True})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Truck Confirmed',
                'message': f'Truck {self.name} has been confirmed and activated.',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def _get_mad_currency(self):
        """Get MAD currency or fallback to company currency"""
        mad_currency = self.env['res.currency'].search([('name', '=', 'MAD')], limit=1)
        return mad_currency if mad_currency else self.env.company.currency_id

    def action_update_odometer(self):
        """Action to update truck odometer"""
        return {
            'name': 'Update Odometer',
            'type': 'ir.actions.act_window',
            'res_model': 'truck.odometer.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_truck_id': self.id,
                'default_current_odometer': self.odometer,
            }
        }