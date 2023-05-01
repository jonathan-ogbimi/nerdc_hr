# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero

from odoo.addons import decimal_precision as dp


class HrExpense(models.Model):
    _inherit = "hr.expense"
    
    company_id = fields.Many2one('res.company',
                                 string='Organization',
                                 readonly=True,
                                 states={
                                     'draft': [('readonly', False)],
                                     'refused': [('readonly', False)]
                                 },
                                 default=lambda self: self.env.user.company_id)
    payment_mode = fields.Selection(
        [("own_account", "Employee (to reimburse/for approval)"),
         ("company_account", "Organization")],
        default='own_account',
        states={
            'done': [('readonly', True)],
            'approved': [('readonly', True)],
            'reported': [('readonly', True)]
        },
        string="Paid By")
    product_id = fields.Many2one('product.product',
                                 string='Product',
                                 readonly=True,
                                 states={
                                     'draft': [('readonly', False)],
                                     'reported': [('readonly', False)],
                                     'refused': [('readonly', False)]
                                 },
                                 required=True, domain=lambda self: self._get_expense_ids())

    unit_amount = fields.Float("Unit Price",
                               readonly=True,
                               required=True,
                               states={
                                   'draft': [('readonly', False)],
                                   'reported': [('readonly', False)],
                                   'refused': [('readonly', False)]
                               },
                               digits=dp.get_precision('Product Price'))
    quantity = fields.Float(required=True,
                            readonly=True,
                            states={
                                'draft': [('readonly', False)],
                                'reported': [('readonly', False)],
                                'refused': [('readonly', False)]
                            },
                            digits=dp.get_precision('Product Unit of Measure'),
                            default=1)
    num_persons = fields.Integer('Number of Persons', default=1,help='Number of persons this expense covers')
    
    state = fields.Selection([('draft', 'To Submit'),
                              ('reported', 'Pending Approval'),
                              ('supervisor', 'Approved By Supervisor'),
                              ('director', 'Approved By Director'),
                              ('approved', 'Approved by Chairman'),
                              ('done', 'Paid'), ('refused', 'Refused')],
                             compute='_compute_state',
                             string='Status',
                             copy=False,
                             index=True,
                             readonly=True,
                             store=True,
                             help="Status of the expense.")
    
    @api.model
    def _get_expense_ids(self):
        domain_filter = [('can_be_expensed', '!=', True)]
        #domain_filter = [('id', '=', 0)]
        user = self.env.user
        ids = []
        #if self.user_has_groups('hr_expense.group_hr_expense_manager') or self.user_has_groups('account.group_account_user') or self.user_has_groups('nerdc_hr.group_hr_expense_director') :
        #    return domain_filter
        
        if self.env.user.employee_ids:
            employee = user.employee_ids[0]
            if employee.grade_id:
                grade = employee.grade_id
                if grade.expense_product_ids:
                    ids = [e.id for e in grade.expense_product_ids]
                    #ids.append(e.id)
                    domain_filter = [('id', 'in', ids)]
        
        return domain_filter


class HrExpenseSheet(models.Model):
    """
        Here are the rights associated with the expense flow

        Action       Group                   Restriction
        =================================================================================
        Submit      Employee                Only his own
                    Officer                 If he is expense manager of the employee, manager of the employee
                                             or the employee is in the department managed by the officer
                    Manager                 Always
        Approve     Officer                 Not his own and he is expense manager of the employee, manager of the employee
                                             or the employee is in the department managed by the officer
                    Manager                 Always
        Post        Anybody                 State = approve and journal_id defined
        Done        Anybody                 State = approve and journal_id defined
        Cancel      Officer                 Not his own and he is expense manager of the employee, manager of the employee
                                             or the employee is in the department managed by the officer
                    Manager                 Always
        =================================================================================
    """
    _inherit = "hr.expense.sheet"
    state = fields.Selection([('draft', 'Draft'), ('submit', 'Submitted'),
                              ('supervisor', 'Approved By Supervisor'),
                              ('director', 'Approved By Director'),
                              ('approve', 'Approved By Chairman'),
                              ('post', 'Posted'), ('done', 'Paid'),
                              ('cancel', 'Refused')],
                             string='Status',
                             index=True,
                             readonly=True,
                             track_visibility='onchange',
                             copy=False,
                             default='draft',
                             required=True,
                             help='Expense Report State')
    user_id = fields.Many2one('res.users',
                              'Director',
                              readonly=True,
                              copy=False,
                              states={'draft': [('readonly', False)]},
                              track_visibility='onchange',
                              oldname='responsible_id')
    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
        copy=False,
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1))
    
    supervisor_user_id = fields.Many2one('res.users',
                              'Supervisor',
                              readonly=True,
                              states={'draft': [('readonly', False)]},
                              copy=False,
                              default = lambda self: self._get_default_supervisor_id(),limit=1)
    
    director_user_id = fields.Many2one('res.users',
                              'Director',
                              readonly=True,
                              states={'draft': [('readonly', False)]},
                              copy=False,
                              default = lambda self: self.env.user.id,limit=1)
    
    num_persons = fields.Integer('Number of Persons', default = 1)
    
#@api.multi
    def approved_by_supervisor(self):
        self.write({'state': 'supervisor','supervisor_user_id':self.env.user.id})
    
#@api.multi
    def approved_by_director(self):
        self.write({'state': 'director','director_user_id':self.env.user.id})
    
    @api.model
    def _get_default_supervisor_id(self):
        user = self.env.user
        if self.env.user.employee_ids:
            employee = user.employee_ids[0]
            if employee.parent_id:
                return employee.parent_id.user_id.id
    @api.model
    def _get_default_director_id(self):
        user = self.env.user
        if self.env.user.employee_ids:
            employee = user.employee_ids[0]
            if employee.parent_id:
                return employee.parent_id.user_id.id
    def activity_update(self):
        for expense_report in self.filtered(lambda hol: hol.state == 'submit'):
            self.activity_schedule(
                'hr_expense.mail_act_expense_approval',
                user_id=expense_report.sudo()._get_responsible_for_approval().id or self.env.user.id)
        self.filtered(lambda hol: hol.state == 'approve').activity_feedback(['hr_expense.mail_act_expense_approval'])
        self.filtered(lambda hol: hol.state == 'supervisor').activity_feedback(['hr_expense.mail_act_expense_approval'])
        self.filtered(lambda hol: hol.state == 'director').activity_feedback(['hr_expense.mail_act_expense_approval'])
        self.filtered(lambda hol: hol.state == 'cancel').activity_unlink(['hr_expense.mail_act_expense_approval'])
