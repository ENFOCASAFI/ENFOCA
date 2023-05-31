# -*- coding: utf-8 -*-

{
	'name': 'Campos para faturas no domiciliados',
	'version': '15.0.1.0.0',
	'category': 'Extra Tools',
	'summary': 'Agrega campos para las facturas no comicilados, campos necesarios para el LE 0802',
	'author': 'Alvpercon',
	'website': 'https://www.alvpercon.com',
	'depends': ['account','solse_pe_cpe'],
	'data': [
		"security/ir.model.access.csv",
		'views/account_move_view.xml',
	],
	'installable': True,
	'sequence': 1,
}