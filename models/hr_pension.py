# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)

PENSION_ARRANGEMENT_CATEGORY = [
    ('contributory', 'Contributory'),
    ('ptad', 'Pension Transitional Arrangement Directorate (PTDA)'),
]


class Employee(models.Model):
    _inherit = 'hr.employee'
    pfa_line_ids = fields.One2many(
        'hr.employee.pfa.line', 'employee_id', string='PFA',
        tracking=True)


class EmployeePFALines(models.Model):
    _name = "hr.employee.pfa.line"
    _sql_constraints = [
        ('uniq_employee_pfa_line', 'unique(type_id,employee_id,hmo_number)',
         "HMO must be unique for each line per employee"),
    ]
    pfa_id = fields.Many2one(
        'hr.employee.pfa', string='Pension Fund Administrator',required=True)
    employee_id = fields.Many2one(
        'hr.employee', 'Employee', tracking=True)
    rsa_number = fields.Char(required=True, string="RSA Number", tracking=True)
    pension_category = fields.Selection(selection=PENSION_ARRANGEMENT_CATEGORY,string="Pension Arrangement Category", help="Select the pension arrangement category",required=True)


class PensionFundAdministrator(models.Model):
    _name = "hr.employee.pfa"
    _description = 'Pension Fund Administrator'
    _sql_constraints = [
        ('uniq_pfa_name', 'unique(name)',
         "PFA Name must be unique"),
    ]
    name = fields.Char('Name', required=True)
