from odoo import models, fields, api, _
from datetime import datetime

class HrContract(models.Model):
    _inherit = "hr.contract"
    _description = 'Entitlements'

    name = fields.Char('Reference Number', required=True)
    contract_wage = fields.Monetary(
        'Entitlement Wage', compute='_compute_contract_wage')
    contract_type_id = fields.Many2one('hr.contract.type', "Entitlement Type")
    recommendation = fields.Text('Supervisor Recommendation', required=False)
    current_job_id = fields.Many2one('hr.job', compute='_compute_employee_contract', store=True, readonly=False,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", string='Current Cadre')
    job_id = fields.Many2one('hr.job', store=True, readonly=False,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", string='Proposed Cadre')
    grade_id = fields.Many2one('hr.grade', string='Proposed CONRAISS')
    request_letter_upload_file = fields.Binary(string='Letter of Request',required=False,tracking=True)
    request_letter_file_name = fields.Char(string='Letter of Request',tracking=True)
    additional_cert_upload_file = fields.Binary(string='Additional Certificate',tracking=True)
    additional_cert_file_name = fields.Char(string='Additional Certificate',tracking=True)
    request_date = fields.Date('Request Date',
        help="Date of request of the entitlement",tracking=True)
    approval_date = fields.Date('Approval Date',
        help="Date of approval of the entitlement")
    state = fields.Selection([
        ('draft', 'Pending'),
        ('probation', 'Probation'),
        ('es', 'Approved by ES'),
        ('board', 'Approved by Board'),
        ('open', 'Approved'),
        ('close', 'Expired'),
        ('cancel','Cancelled'),
        ('trash', 'Trashed'),
    ], string='Status', group_expand='_expand_states', copy=False,
       tracking=True, help='Status of the entitlement', default='draft')
    
    """
    
    @api.model
    def create(self, vals_list):
    
        function for create a record based on probation
        details in a model
        
        if vals_list['trial_date_end'] and vals_list['state'] == 'probation':
            dtl = self.env['hr.training'].create({
                'employee_id': vals_list['employee_id'],
                'start_date': vals_list['date_start'],
                'end_date': vals_list['trial_date_end'],
            })
            vals_list['probation_id'] = dtl.id
        
        res = super(HrContract, self).create(vals_list)
        return res
    """
    def action_approve(self):
        """
        function used for changing the state probation into
        running when approves a contract
        """

        self.write({'is_approve': True})
        if self.state == 'probation':
            self.write({'state': 'open',
                        'is_approve': False})
    
    def action_running(self):
        """
        function used for changing the state probation into
        running when approves a contract
        """

        self.write({'state': 'open'})

    def action_approved_by_es(self):
        """
        function used for changing the state probation into
        running when approves a contract
        """

        self.write({'is_approve': True, 'state': 'es','approval_date':datetime.today()})
        # if self.state=='draft' :
        #    self.write({'state': 'open',
        #                'is_approve': False})

    def action_approved_by_board(self):
        """
        function used for changing the state probation into
        running when approves a contract
        """

        self.write({'is_approve': True, 'state': 'board','approval_date':datetime.today()})
    
    def action_expired(self):
        """
        function used for changing the state probation into
        running when approves a contract
        """

        self.write({'is_approve': True, 'state': 'close'})
    
    def action_cancelled(self):
        """
        function used for changing the state probation into
        running when approves a contract
        """

        self.write({'is_approve': True, 'state': 'trash'})

    def action_set_probation(self):
        """
        function used for changing the state probation into
        running when approves a contract
        """

        self.write({'is_approve': False,'state':'probation'})
  
  