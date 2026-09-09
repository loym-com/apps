{
    'name': 'Generic Accounting Reports',
    'version': '1.0',
    'category': 'Accounting',
    'depends': [
        'account',
    ],
    'data': [
        # 'views/account_report_views.xml',
        'data/account_report_data.xml',
    ],
    'license': 'LGPL-3',
    'author': 'Loym',
    "description": "account.report does not work on Community Edition, since there is no client action / javascript to process account_report. it is only available in the Enterprise Edition.",
}
