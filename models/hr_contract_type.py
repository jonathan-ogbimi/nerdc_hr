# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ContractType(models.Model):
    _inherit = 'hr.contract.type'
    _description = 'Entitlement Type'
   
    name = fields.Char(string='Entitlement Type', required=True, help="Name")
    sequence = fields.Integer(help="Gives the sequence when displaying a list of Entitlement.", default=10)