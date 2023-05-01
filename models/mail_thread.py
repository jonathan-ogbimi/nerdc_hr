# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import models, fields, api, _


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'
    message_is_follower = fields.Boolean('Is Copied',
                                         compute='_compute_is_follower',
                                         search='_search_is_follower')
    message_follower_ids = fields.One2many(
        'mail.followers',
        'res_id',
        string='Copied',
        domain=lambda self: [('res_model', '=', self._name)])
    message_partner_ids = fields.Many2many(comodel_name='res.partner',
                                           string='Copied (Partners)',
                                           compute='_get_followers',
                                           search='_search_follower_partners')
    message_channel_ids = fields.Many2many(comodel_name='mail.channel',
                                           string='Copied (Channels)',
                                           compute='_get_followers',
                                           search='_search_follower_channels')
