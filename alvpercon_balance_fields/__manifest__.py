# -*- coding: utf-8 -*-

{
	'name': 'Campos para creación de balance en contbilidad',
	'version': '15.0.1.0.0',
	'category': 'Extra Tools',
	'summary': 'Agrega campos y wizard, ´se crea un listado con comandos sql de postgres',
	'author': 'Alvpercon',
	'website': 'https://www.alvpercon.com',
	'depends': ['account'],
	'data': [
		"security/ir.model.access.csv",		
		'wizard/balance_date_view.xml',
		'views/balance_record_group.xml',
		'views/balance_record_group_periodo.xml',
		'views/balance_record_group_dolar.xml',
		# 'views/balance_record_group.dolar.xml',
	],
	'installable': True,
	'sequence': 1,
}