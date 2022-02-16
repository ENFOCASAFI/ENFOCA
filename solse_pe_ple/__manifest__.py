# -*- coding: utf-8 -*-

{
	'name': 'PLE SUNAT - Base',
	'version': '14.0.1.0.0',
	'category': 'Technical Configuration',
	'summary': 'Base para la declaración de PLE a SUNAT',
	'depends': [
		'solse_pe_edi',
		'solse_pe_cpe',
		'solse_pe_cpe_guias',
	],
	'data': [
		'security/ir.model.access.csv',
		'security/sunat_ple_security.xml',
		'views/account_analytic_views.xml',
		'views/res_partner_views.xml',
		'views/account_payment_views.xml',
		'views/res_bank_views.xml',
		'views/ple_report_views.xml',
		'views/ple_report_01_view.xml',
		'views/ple_menu_view.xml',
	],
	'external_dependencies': {
		'python': [
			'pandas',
			'xlsxwriter',
		],
	},
	'auto_install': False,
	'installable': True,
	'application': True,
	'sequence': 1,
}
