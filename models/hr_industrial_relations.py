# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _inherit = 'hr.employee'
    union_line_ids = fields.One2many(
        'hr.employee.ir.line', 'employee_id', string='Industrial Relations',
        tracking=True)


class EmployeeUnionLines(models.Model):
    _name = "hr.employee.ir.line"
    _sql_constraints = [
        ('uniq_employee_pfa_line', 'unique(type_id,employee_id,hmo_number)',
         "HMO must be unique for each line per employee"),
    ]
    union_id = fields.Many2one(
        'hr.employee.ir', string='Industrial Relation', required=True)
    employee_id = fields.Many2one(
        'hr.employee', 'Employee', tracking=True)
    membership_number = fields.Char(
        required=True, string="Membership Number", tracking=True)
    financial_obligation = fields.Float(
        required=True, digits=dp.get_precision('Product Price'), default=0)


class EmployeeUnion(models.Model):
    _name = "hr.employee.ir"
    _description = 'Industrial Union'
    _sql_constraints = [
        ('uniq_union_name', 'unique(name)',
         "Union Name must be unique"),
    ]
    name = fields.Char('Name', required=True)
    type_id = fields.Many2one(
        'hr.employee.ir.type', 'Union Type', tracking=True)


class UnionType(models.Model):
    _name = "hr.employee.ir.type"
    _description = 'Union Type'
    _sql_constraints = [
        ('uniq_union_type_name', 'unique(name)',
         "Union Type Name must be unique"),
    ]
    name = fields.Char('Name', required=True)
