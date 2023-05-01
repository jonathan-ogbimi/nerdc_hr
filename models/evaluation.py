# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import models, fields, api, _


class HrJob(models.Model):
    _inherit = "hr.job"
    kra_id = fields.Many2one('hr.kra', 'Evaluation')
