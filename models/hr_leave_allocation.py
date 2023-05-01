# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import models, fields, api, _


class HrLeaveAllocation(models.Model):
    _inherit = "hr.leave.allocation"
    # mode
    holiday_type = fields.Selection([
        ('employee', 'By Employee'),
        ('company', 'By Organization'),
        ('department', 'By Department/Unit'),
        ('category', 'By Employee Tag')],
        string='Allocation Mode', readonly=True, required=True, default='employee',
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
        help="Allow to create requests in batchs:\n- By Employee: for a specific employee"
             "\n- By Organization: all employees of the specified company"
             "\n- By Department: all employees of the specified department"
             "\n- By Employee Tag: all employees of the specific employee group category")
    mode_company_id = fields.Many2one(
        'res.company', string='Organization', readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    department_id = fields.Many2one(
        'hr.department', string='Department/Unit', readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})