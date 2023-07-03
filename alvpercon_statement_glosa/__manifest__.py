# -*- coding: utf-8 -*-

{
	'name': 'Glosa desde extractos bancarios',
	'version': '15.0.1.0.0',
	'category': 'Extra Tools',
	'summary': 'crea un campo que relaciona las lineas de extractos bancarios con los asientos contables (campos de encabezado)',
	'author': 'Alvpercon',
	'website': 'https://www.alvpercon.com',
	'depends': ['account'],
	'data': [
		#"security/ir.model.access.csv",
		'views/account_move_view.xml',
	],
	'installable': True,
	'sequence': 1,
}