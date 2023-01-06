# -*- coding: utf-8 -*-

{
	'name': 'Campos destino tipo boolean',
	'version': '0.0.1',
	'category': 'Extra Tools',
	'summary': '''Crea campo de destino de tipo booleano en account.move.line
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
