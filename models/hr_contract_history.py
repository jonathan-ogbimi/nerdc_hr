# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from collections import defaultdict


class ContractHistory(models.Model):
    _inherit = 'hr.contract.history'
    _description = 'Entitlement History'
    # Even though it would have been obvious to use the reference contract's id as the id of the
    # hr.contract.history model, it turned out it was a bad idea as this id could change (for instance if a
    # new contract is created with a later start date). The hr.contract.history is instead closely linked
    # to the employee. That's why we will use this id (employee_id) as the id of the hr.contract.history.
    name = fields.Char('Entitlement Name', readonly=True)
   
    is_under_contract = fields.Boolean('Is Currently Under Entitlement', readonly=True)
    job_id = fields.Many2one('hr.job', string='Proposed Cadre', readonly=True)
    state = fields.Selection([
        ('draft', 'Pending'),
        ('probation', 'Probation'),
        ('es', 'Approved by ES'),
        ('board', 'Approved by Board'),
        ('open', 'Approved'),
        ('close', 'Expired'),
        ('cancel','Cancelled'),
        ('trash', 'Trashed'),
    ], string='Status', readonly=True)
  
    contract_type_id = fields.Many2one('hr.contract.type', 'Entitlement Type', readonly=True)
    contract_ids = fields.One2many('hr.contract', string='Entitlements', compute='_compute_contract_ids', readonly=True, compute_sudo=True)
    contract_count = fields.Integer(compute='_compute_contract_count', string="# Entitlements")
    under_contract_state = fields.Selection([
        ('done', 'Under Entitlement'),
        ('blocked', 'Not Under Entitlement')
    ], string='Contractual Status', compute='_compute_under_contract_state')


   