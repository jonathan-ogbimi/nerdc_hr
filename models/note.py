from odoo import api, fields, models, _
from odoo.tools import html2plaintext


class Note(models.Model):
    _inherit = 'note.note'
    _description = "Internal Note"

    name = fields.Text(compute='_compute_name',
                       string='Memo Summary', store=True)
    memo = fields.Html('Memo Content')
    #digital_signature = fields.Binary(string='Signature')

    @api.model
    def _get_current_user(self):
        for rec in self:
            rec.current_user = self.env.user
        # i think this work too so you don't have to loop
        self.update({'current_user': self.env.user.id})

    @api.model
    def _get_user_id(self):
        return self.env.uid

    @api.depends('user_id')
    def _note_updatable(self):
        for line in self:
            if line.user_id == self.env.uid:
                line.note_updatable = True
