# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import models, fields, api, _


class HrGrade(models.Model):
    _inherit = "hr.grade"
    is_above_manager = fields.Boolean(
        'Is A Director', help="Tick this if grade is Director level.")
    hr_job_ids = fields.Many2many('hr.job')
    expense_product_ids = fields.Many2many('product.product',domain = [('can_be_expensed', '=', True)])
    leave_type_ids = fields.Many2many('hr.leave.type')


class Products(models.Model):
    _inherit = "product.product"
    grade_id = fields.Many2one('hr.grade', string='Grade')
