# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Employee(models.Model):
    _inherit = "hr.employee"
    _sql_constraints = [
        ('uniq_identification_id_ref', 'unique(identification_id)',
         "An employee exists with this Identification ID"),
        ('uniq_employment_id_ref', 'unique(employment_id)',
         "An employee exists with this Employment Number"),
         ('uniq_id_card_ref', 'unique(card_number)',
         "An employee exists with this ID Card Number")

    ]

    employment_id = fields.Char(
        string='Employment Number', track_visibility='always', required=True)
    card_number = fields.Char(
        string='ID Card Number', track_visibility='always', required=True)
    firstname = fields.Char(string='First Name',
                            track_visibility='always', required=True)
    middlename = fields.Char(string='Middle Name', track_visibility='always')
    lastname = fields.Char(string='Last Name', track_visibility='always')
    parent_id = fields.Many2one('hr.employee', 'Supervisor')
    state_id = fields.Many2one('res.country.state', 'State of Origin')
    lga_id = fields.Many2one('hr.lga', 'Local Government')
    title = fields.Many2one('hr.title', 'Title', required=True)
    deployment_station = fields.Many2one(
        'res.country.state', 'Station of Deployment', track_visibility='always')
    department_id = fields.Many2one(
        'hr.department', 'Department/Unit', track_visibility='always')
    manager = fields.Boolean(string='Is a Director')
    kra_id = fields.Many2one('hr.kra',
                             related='job_id.kra_id',
                             string="Evaluation",
                             readonly=True)
    joining_date = fields.Date(string='Date of First Appointment')
    service_years = fields.Integer(string='Length of Service (yrs)')
    retirement_date = fields.Date(
        string='Retirement Date', track_visibility='always')
    academic_category = fields.Selection([
        ('academic', 'Academic/Teaching'),
        ('non_academic', 'Non-Academic'),
    ], groups="hr.group_hr_user", string='Academic Category', tracking=True)
    grade_id = fields.Many2one('hr.grade', 'CONRAISS Level/Grade')
    present_appointment_date = fields.Date(
        string='Date of Present Appointment', track_visibility='always')
    confirmation_date = fields.Date(
        'Date of Confirmation', groups="hr.group_hr_user", track_visibility='always')
    promotion_date = fields.Date(
        'Date of Promotion', groups="hr.group_hr_user", track_visibility='always')
    vehicle = fields.Char(string='Vehicle Plate Number')
    expense_manager_id = fields.Many2one(
        'res.users', string='Expense Director Approval',
        domain=lambda self: [('groups_id', 'in', self.env.ref(
            'nerdc_hr.group_hr_expense_director').id)],
        help="User responsible of expense approval. Should be Expense Director.")

    # @api.multi
    def write(self, vals):
        updated_vals = self.update_name(vals)
        employee = super(Employee, self).write(updated_vals)
 
        return employee

    #@api.multi
    def set_title(self):
        for e in self:
            e.write({
            'name': '%s %s' % (self.title.name, self.name)
        })
    # @api.multi

    def update_name(self, vals):
        '''
         iden_no = vals[
            'identification_id'] if 'identification_id' in vals else self.identification_id
        '''
        title_id =  vals['title'] if 'title' in vals else self.title.id
        titles = self.env['hr.title'].search([('id', '=', title_id)],limit=1)
        for t in titles:
            fname = vals['firstname'] if 'firstname' in vals else (
                self.firstname or '')
            midname = vals['middlename'] if 'middlename' in vals else (
                self.middlename or '')
            lname = vals['lastname'] if 'lastname' in vals else (
                self.lastname or '')
            name = "%s %s %s %s" % (t.name,fname, midname, lname)
            if 'name' in vals:
                vals['name'] = name.replace('False', '')
        return vals

    @api.model
    def create(self, vals):
        updated_vals = self.update_name(vals)
        employee = super(Employee, self).write(updated_vals)
        return employee

    @api.onchange('first_contract_date')
    def _onchange_start_date(self):
        date = self.first_contract_date
        # length of service = 35 years
        delta = relativedelta(years=35)
        date += delta
        self.retirement_date = date

    '''
    
    @api.depends('first_contract_date', 'retirement_date')
    def _compute_retirement_date(self):
        for record in self:
            date = record.first_contract_date
            # length of service = 35 years
            delta = relativedelta(years=35)
            date += delta
            record.retirement_date = date
    '''

    @api.depends('firstname', 'lastname', 'middlename', 'name')
    def _compute_name(self):
        for employee in self:
            employee.name = '%s %s %s' % (
                employee.firstname, employee.middlename, employee.lastname)

    @api.depends('contract_ids.state', 'contract_ids.date_start')
    def _compute_first_contract_date(self):
        for employee in self:
            today = fields.Date.today()
            employee.first_contract_date = employee._get_first_contract_date()
            date = employee.first_contract_date
            # 35 years length of service
            delta = relativedelta(years=35)
            date += delta
            employee.retirement_date = date
            difference_in_years = relativedelta(
                today, employee.first_contract_date, ).years
            employee.service_years = difference_in_years


class Department(models.Model):
    _inherit = "hr.department"
    name = fields.Char('Department/Unit Name', required=True)
    _description = "Department/Units"
    parent_id = fields.Many2one('hr.department',
                                string='Parent Department/Unit',
                                index=True)
    child_ids = fields.One2many(
        'hr.department', 'parent_id', string='Child Departments/Units')
    manager_id = fields.Many2one('hr.employee',
                                 string='Supervisor',
                                 track_visibility='onchange')
    company_id = fields.Many2one('res.company', string='Organization',
                                 index=True, default=lambda self: self.env.user.company_id)
    leave_to_approve_count = fields.Integer(
        compute='_compute_leave_count', string='Leave to Approve')


class Job(models.Model):

    _inherit = "hr.job"
    department_id = fields.Many2one('hr.department', string='Department/Unit')
    company_id = fields.Many2one(
        'res.company', string='Organization', default=lambda self: self.env.user.company_id)


class HrLocalGovernment(models.Model):
    _name = "hr.lga"
    _description = 'Local Governments'
    name = fields.Char('LGA Name', required=True)
    state_id = fields.Many2one('res.country.state', 'State of Origin')


class EmployeeTitle(models.Model):
    _name = "hr.title"
    _description = 'Title'
    name = fields.Char('Title Name', required=True)
