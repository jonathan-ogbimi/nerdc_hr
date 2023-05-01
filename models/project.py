
from odoo import models, fields, api


class Task(models.Model):
    _inherit = "project.task"
    completion_notes = fields.Html(string='Completion Notes')
    report_upload_file = fields.Binary(
        string='Report Attachment', tracking=True)
    report_file_name = fields.Char(
        string='Report Attachment', tracking=True)
