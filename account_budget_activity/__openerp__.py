# -*- coding: utf-8 -*-
{
    'name': 'Activity Based Budgets Management',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """

Activity based budgetting

""",
    'author': 'Kitti U.',
    'website': 'http://ecosoft.co.th',
    'depends': [
        'account',
        'purchase',
        'purchase_requisition',
        'purchase_request',
        'purchase_request_to_requisition',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/account_budget_security.xml',
        'views/purchase_view.xml',
        'views/purchase_requisition_view.xml',
        'views/purchase_request_view.xml',
        'views/account_budget_view.xml',
        'views/account_activity_view.xml',
        'views/purchase_view.xml',
        'views/account_view.xml',
        'views/account_invoice_view.xml',
        'views/account_move_line_view.xml',
        'views/analytic_view.xml',
        'wizard/purchase_request_line_make_purchase_requisition_view.xml',
        'workflow/account_budget_workflow.xml',
    ],
    'demo': [
        'demo/activity_demo.xml',
        'demo/account_budget_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
