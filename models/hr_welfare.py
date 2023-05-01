# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _inherit = 'hr.employee'
    welfare_line_ids = fields.One2many(
        'hr.employee.welfare.line', 'employee_id', string='Welfare Packages',
        tracking=True)
    hmo_line_ids = fields.One2many(
        'hr.employee.hmo.line', 'employee_id', string='HMO',
        tracking=True)


class EmployeeWelfareLines(models.Model):
    _name = "hr.employee.welfare.line"
    _sql_constraints = [
        ('uniq_employee_welfare', 'unique(type_id,employee_id)',
         "Welfare Type must be unique for each line per employee"),
    ]
    type_id = fields.Many2one(
        'hr.employee.welfare.type', string='Welfare Type')
    employee_id = fields.Many2one(
        'hr.employee', 'Employee', tracking=True)
    amount = fields.Float(
        required=True, digits=dp.get_precision('Product Price'), default=0)


class EmployeeHMOLines(models.Model):
    _name = "hr.employee.hmo.line"
    _sql_constraints = [
        ('uniq_employee_welfare', 'unique(type_id,employee_id,hmo_number)',
         "HMO must be unique for each line per employee"),
    ]
    hmo_id = fields.Many2one(
        'hr.employee.hmo', string='HMO')
    employee_id = fields.Many2one(
        'hr.employee', 'Employee', tracking=True)
    hmo_number = fields.Char(required=True,string='HMO Number', tracking=True)


class WelfareType(models.Model):
    _name = "hr.employee.welfare.type"
    _description = 'Welfare Type'
    _sql_constraints = [
        ('uniq_welfare_type_name', 'unique(name)',
         "Welfare Type must be unique"),
    ]
    name = fields.Char('Name', required=True)


class HMO(models.Model):
    _name = "hr.employee.hmo"
    _description = 'Health Maintenance Organization'
    _sql_constraints = [
        ('uniq_hmo_name', 'unique(name)',
         "HMO Name must be unique"),
    ]
    name = fields.Char('Name', required=True)
