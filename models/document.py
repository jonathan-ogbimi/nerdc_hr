# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

DOCUMENT_STATES = [
    ('draft', 'Pending'),
    ('assigned', 'Assigned'),
    ('done', 'Put Away'),
    ('archived', 'Archived'),
]


class Document(models.Model):
    _inherit = "document.document"
    _sql_constraints = [
        ('uniq_file_number_ref', 'unique(file_number)',
         "File Number must be unique"),
    ]
    name = fields.Char('Title', required=True, tracking=True)
    description = fields.Text('Subject Matter', required=True, tracking=True)
    file_number = fields.Char(
        string="File Number", required=True, tracking=True)
    volume_number = fields.Char(
        string="Volume Number", required=True, tracking=True)
    doc_upload_file = fields.Binary(
        string='Attachment', required=True, tracking=True)
    doc_file_name = fields.Char(string='Attachment', tracking=True)
    state = fields.Selection(selection=DOCUMENT_STATES, string='Status', copy=False,
                             tracking=True, help='Status of the document', default='draft')
    department_id = fields.Many2one(
        'hr.department', 'Destination Department/Unit', required=True, tracking=True)
    type_id = fields.Many2one(
        'document.type', string='Document Type', readonly=False)
    employee_id = fields.Many2one(
        'hr.employee', 'Receiver Staff', required=True, tracking=True)
    sheet_ids = fields.One2many(
        'document.action.sheet', 'document_id', string='Action Sheet')
    count_sheets = fields.Integer(
        "Number of Action Sheets", compute="_compute_count_sheets"
    )

    def action_assign(self):
        self.write({'state': 'assigned'})

    def action_put_away(self):
        self.write({'state': 'done'})

    def action_archive(self):
        self.write({'state': 'archived'})

    def action_draft(self):
        self.write({'state': 'draft'})

    @api.depends("sheet_ids")
    def _compute_count_sheets(self):
        for r in self:
            r.count_sheets = len(r.sheet_ids)

    def action_activity_sheet(self):
        # target = self, new
        return {
            'name': _('Action Sheets'),
            'view_type': 'tree',
            'view_mode': 'tree,form',
            'domain': [('document_id', '=', self.id)],
            'view_id': self.env.ref('nerdc_hr.view_document_action_sheet_tree').id,
            'res_model': 'document.action.sheet',
            'context': "{'default_document_id':'%s'}" % (self.id),
            'type': 'ir.actions.act_window',
            'target': 'self',
        }

    # filter employees based on department
    @api.onchange('department_id')
    def filter_employees(self):
        for rec in self:
            return {'domain': {'employee_id': [('department_id', '=', rec.department_id.id)]}}


class DocumentType(models.Model):
    _name = "document.type"
    _description = 'Document Type'
    name = fields.Char('Name', required=True)


class DocumentActionSheet(models.Model):
    _name = "document.action.sheet"
    _description = 'Action Sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char('Folio', required=True, tracking=True)
    document_id = fields.Many2one(
        'document.document', 'Document', tracking=True)
    employee_id = fields.Many2one(
        'hr.employee', 'Receiver Staff', tracking=True)
    department_id = fields.Many2one(
        'hr.department', 'Destination Department/Unit', tracking=True)
    start_date = fields.Date('Date From', help="Start date", tracking=True)
    end_date = fields.Date('Date To', help="End date", tracking=True)
    sender_notes = fields.Text('Sender Notes')
    notes = fields.Text('Action Notes')
    acknowledged = fields.Boolean('Acknowledged', tracking=True)
    state = fields.Selection(selection=DOCUMENT_STATES, string='Status', copy=False,
                             tracking=True, help='Status of the action sheet', default='draft')

    def action_assign(self):
        for e in self:
            e.write({'state': 'assigned'})
            doc = e.document_id
            doc.write({'state': 'assigned'})

    def action_put_away(self):
        for e in self:
            e.write({'state': 'done'})
            doc = e.document_id
            doc.write({'state': 'done'})

    def action_archive(self):
        for e in self:
            e.write({'state': 'archived'})
            e.document_id.write({'state': 'archived'})

    def action_draft(self):
        for e in self:
            e.write({'state': 'draft'})
            e.document_id.write({'state': 'draft'})

    # filter employees based on department

    @api.onchange('department_id')
    def filter_employees(self):
        for rec in self:
            return {'domain': {'employee_id': [('department_id', '=', rec.department_id.id)]}}
