# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import models, fields, api, _


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    leave_manager_id = fields.Many2one(
        'res.users', string='Leave Supervisor',
        compute='_compute_leave_manager', store=True, readonly=False,
        domain="[('share', '=', False), ('company_ids', 'in', company_id)]",
        help='Select the user responsible for approving "Leave" of this employee.\n'
             'If empty, the approval is done by an Administrator or Approver (determined in settings/users).')
    remaining_leaves = fields.Float(
        compute='_compute_remaining_leaves', string='Remaining Paid Leave',
        help='Total number of paid time off allocated to this employee, change this value to create allocation/time off request. '
             'Total based on all the time off types without overriding limit.')
    current_leave_state = fields.Selection(compute='_compute_leave_status', string="Current Leave Status",
                                           selection=[
                                               ('draft', 'New'),
                                               ('confirm', 'Waiting Approval'),
                                               ('refuse', 'Refused'),
                                               ('validate1',
                                                'Waiting Second Approval'),
                                               ('validate', 'Approved'),
                                               ('cancel', 'Cancelled')
                                           ])
    leaves_count = fields.Float(
        'Number of Leave', compute='_compute_remaining_leaves')

class HrLeave(models.Model):
    _inherit = "hr.leave"
    _description = "Leave"
    handover_note = fields.Text('Handover Notes')
    manager_id = fields.Many2one(
        'hr.employee', string='Supervisor', readonly=True)
    handover_employee_id = fields.Many2one(
        'hr.employee', string='Handover Employee', required=True)
    request_unit_half = fields.Boolean('Half Day', readonly=True)
    director_note = fields.Text('Approval Notes')
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'Awaiting Approval'),
        ('refuse', 'Refused'),
        ('validate1', 'Approved by Supervisor'),
        ('validate', 'Approved by HR')
    ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='confirm',
        help="The status is set to 'To Submit', when a leave request is created." +
        "\nThe status is 'Awaiting Approval', when leave request is confirmed by user." +
        "\nThe status is 'Refused', when leave request is refused by manager." +
        "\nThe status is 'Approved by Supervisor', when leave request is approved by supervisor.")
    # domain=lambda self: self._get_leave_type_ids(),domain=[('valid', '=', True)]
    # leave type configuration
    holiday_status_id = fields.Many2one(
        "hr.leave.type", compute='_compute_from_employee_id', store=True, string="Leave Type", required=True, readonly=False,
        states={'cancel': [('readonly', True)], 'refuse': [('readonly', True)], 'validate1': [('readonly', True)], 'validate': [('readonly', True)]},
        domain="[('company_id', '?=', employee_company_id), '|', ('requires_allocation', '=', 'no'), ('has_valid_allocation', '=', True)]")
    '''
    holiday_status_id = fields.Many2one(
        "hr.leave.type", string="Leave Type", required=True, readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [
            ('readonly', False)]},
        domain=lambda self: self._get_leave_type_ids())
    '''
    private_name = fields.Char('Leave Description', groups='hr_holidays.group_hr_holidays_user')
    condition_id = fields.Many2one(
        'hr.leave.approval.condition', string='Condition of Approval',tracking=True, readonly=False)
    resumption_date = fields.Date('Resumption Date',required=True)
    contact_address = fields.Text('Contact Address',required=True)
    contact_phone = fields.Char('Contact Phone',required=True)
    bond_upload_file = fields.Binary(string='Bond Agreement',tracking=True)
    bond_file_name = fields.Char(string='Bond Agreement',tracking=True)

    @api.model
    def _get_leave_type_ids(self):
        domain_filter = [('valid', '=', True)]
        # return domain_filter
        user = self.env.user
        ids = []
        # if self.user_has_groups('hr_expense.group_hr_expense_manager') or self.user_has_groups('account.group_account_user') or self.user_has_groups('nerdc_hr.group_hr_expense_director') :
        #    return domain_filter
        '''
        
        if self.env.user.employee_ids:
            employee = user.employee_ids[0]
            if employee.grade_id:
                grade = employee.grade_id
                if grade.leave_type_ids:
                    ids = [e.id for e in grade.leave_type_ids]
                    #ids.append(e.id)
                    #domain_filter = [('id', 'in', ids)]
                    domain_filter.append(('id', 'in', ids))
                else:
                    # if grade not assigned, cannot select leave type
                    domain_filter.append(('id', '=', 0))
        '''
        return domain_filter
    

class LeaveApprovalCondition(models.Model):
    _name = "hr.leave.approval.condition"
    _description = 'Condition of Approval'
    name = fields.Char('Name', required=True)

