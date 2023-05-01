# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import UserError, ValidationError


class Employee(models.Model):
    _inherit = "hr.employee"
    staff_recruitment_id = fields.Many2one('staff.recruitment', 'Recruitment')


class StaffRequitment(models.Model):
    _inherit = 'staff.recruitment'
    _description = "Employee recruitment"
    applicant_id = fields.Many2one(
        'res.users', string="Applicant User", required=True)
    employment_id = fields.Char(
        string='Employment Number', track_visibility='always')
    card_number = fields.Char(
        string='ID Card Number', track_visibility='always')
    firstname = fields.Char(string='First Name',
                            track_visibility='always')
    middlename = fields.Char(string='Middle Name', track_visibility='always')
    lastname = fields.Char(string='Last Name', track_visibility='always')
    parent_id = fields.Many2one('hr.employee', 'Supervisor')
    title = fields.Many2one('hr.title', 'Title', required=True)
    fitness_cert_upload_file = fields.Binary(
        string='Certificate of Fitness', tracking=True)
    fitness_cert_file_name = fields.Char(
        string='Certificate of Fitness', tracking=True)
    indigene_cert_upload_file = fields.Binary(
        string='Certificate of Indigene', tracking=True)
    indigene_cert_file_name = fields.Char(
        string='Certificate of Indigene', tracking=True)
    application_upload_file = fields.Binary(
        string='Application letter', tracking=True)
    application_file_name = fields.Char(
        string='Application Letter', tracking=True)
    school_details_upload_file = fields.Binary(
        string='School Details', tracking=True)
    school_details_file_name = fields.Char(
        string='School Details', tracking=True)
    age_cert_upload_file = fields.Binary(
        string='Age Declaration', tracking=True)
    age_cert_file_name = fields.Char(string='Age Declaration', tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('approve', 'Approved by Supervisor'),
         ('confirm', 'Approved by HR'),
         ('cancel', 'Cancel')], string='State',
        default='draft')

    def action_confirm(self):
        res_obj = self.env['hr.applicant'].sudo()
        res_obj.create(
            {
                'job_id': self.job_id.id,
                'name': self.job_id.name + '/' + self.sequence,
            }
        )
        self.write({'state': 'confirm'})
        return
