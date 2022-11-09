# -*- coding: utf-8 -*-

{
	'name': 'Campos de diferencia de conversion y tipo de cambio',
	'version': '0.0.1',
	'category': 'Extra Tools',
	'summary': '''Crea campos de diferencia de conversion y tipo de cambio en account.move.line
	para filtrar cuentas que ejecutan ambos procesos
 	''',
	'author': 'Alvpercon',
	'website': 'https://www.alvpercon.com',
	'license': 'LGPL-3',
	'depends': [
		'base',
		'l10n_pe_currency',
		'account',
		'solse_pe_accountant',
	],
	'data': [
		'views/account_move_line_view.xml',
	],
	'installable': True,
	'sequence': 1,
}
