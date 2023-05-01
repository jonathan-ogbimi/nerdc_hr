# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Job(models.Model):

    _description = "Cadre/Job Position"
    _inherit = 'hr.job'
    name = fields.Char(string='Cadre', required=True, index='trigram', translate=True)
    