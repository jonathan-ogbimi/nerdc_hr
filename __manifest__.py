# -*- coding: utf-8 -*-
{
    'name':
    "NERDC HRM",
    'summary':
    """
        HR Customizations for the NERDC""",
    'description':
    """
       HR Customizations for the NERDC
    """,
    'author':
    "Jonathan Ogbimi",
    'website':
    "http://www.encom.com.ng",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':
    'Uncategorized',
    'version':
    '0.1',

    # any module necessary for this one to work correctly
    # 'note_extended','web_digital_sign','hr_grade',
    'depends': [
        'base', 'hr', 'mail', 'calendar', 'hrms_dashboard', 'employee_kra',
        'hr_employee_updation', 'hr_holidays', 'hr_expense', 'account', 'report_xlsx',
        'oh_employee_documents_expiry', 'app_odoo_customize',
        'hr_contract', 'analytic', 'product', 'note', 'hr_contract_types',
        'base_technical_features', 'hr_grade', 'hr_skills',
        'hr_gratuity_settlement', 'hr_resignation', 'employee_recruitment_app', 'document_management_system',
        'project','project_kanban_logo'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/hr_security.xml',
        'security/hr_holidays_security.xml',
        'security/hr_expense_security.xml',
        # 'security/note_security.xml',
        'views/hr_nominal_roll.xml',
        'views/hr_career_progression.xml',
        'views/hr_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_contract_types.xml',
        'views/hr_contract_history_report_views.xml',
        'views/hr_job_views.xml',
        'views/hr_contract_upgrading.xml',
        'views/hr_leave_views.xml',
        'views/hr_disengagement.xml',
        'views/hr_recruitment.xml',
        'views/document.xml',
        'views/hr_welfare.xml',
        'views/hr_pension.xml',
        'views/hr_industrial_relations.xml',
        'views/project.xml',
        'data/data.xml',
        'views/templates.xml',
        # 'views/mail_followers_views.xml',
        # 'wizard/invite_view.xml',
        'views/note_view.xml',
    ],
    # 'qweb': ["static/xml/hrms_dashboard.xml"],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
