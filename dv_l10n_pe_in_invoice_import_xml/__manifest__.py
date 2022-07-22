{
    'name': """
        dv_l10n_pe_in_invoice_import_xml
    """,

    'summary': """
        SUMMARY. |
    """,

    'description': """
        DESCRIPTION. |
    """,

    'author': 'Develogers',
    'website': 'https://develogers.com',
    'support': 'especialistas@develogers.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'category': 'Invoice',
    'version': '14.0',

    'depends': [
        'base',
        'account',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/model_template_views.xml',
        'views/invoice_supplier_import_views.xml',
        'views/menuitem_views.xml',
    ],

    "assets": {
    },

    'images': ['static/description/banner.gif'],

    'application': True,
    'installable': True,
    'auto_install': False,
    'sequence': 1,
}
