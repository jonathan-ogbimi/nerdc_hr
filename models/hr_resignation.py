# -*- coding: utf-8 -*-
import datetime
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

date_format = "%Y-%m-%d"
DISENGAGEMENT_TYPE = [
    ('resigned', 'Normal Resignation'),
    ('abscondment', 'Abscondment'),
    ('termination', 'Termination'),
    ('fired', 'Dismissal'),
]


class HrResignation(models.Model):
    _inherit = 'hr.resignation'
    _description="Disengagement"
    
    name = fields.Char(string='Reference Number', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))

    expected_revealing_date = fields.Date(string="Last Day of Employee", required=True,
                                          help='Employee requested date on which he is revealing from the organization.')
    reason = fields.Text(string="Reason", required=True,
                         help='Specify reason for leaving the disengagement')
    notice_period = fields.Char(string="Notice Period")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Approved by Supervisor'),
         ('approved', 'Approved by HR'),
         ('cancel', 'Rejected')],
        string='Status', default='draft', track_visibility="always")
    resignation_type = fields.Selection(selection=DISENGAGEMENT_TYPE, help="Select the type of resignation: normal "
                                        "resignation, abscondment,terminated or dismissed by the organization")
    employee_contract = fields.Char(String="Entitlement")
    resignation_letter_upload_file = fields.Binary(string='Resignation Letter',tracking=True)
    resignation_letter_file_name = fields.Char(string='Resignation Letter',tracking=True)
    clearance_dept = fields.Boolean(string="Department/Unit")
    clearance_library = fields.Boolean(string="Library")
    clearance_housing = fields.Boolean(string="Housing Committee")
    clearance_school = fields.Boolean(string="Model School")
    clearance_finance = fields.Boolean(string="Finance")
    clearance_hr = fields.Boolean(string="Human Resources")
    clearance_cooperative = fields.Boolean(string="Cooperative Societies")
    
    def approved_by_supervisor(self):
        """
        set resination to approved by supervisor
        """

        self.write({'state': 'supervisor'})
