# -*- coding: utf-8 -*-

{
	'name': 'Actualiza Glosa en asientos de diferencia de cambio y de Conversión',
	'version': '15.0.10.0.5',
	'category': 'Extra Tools',
	'summary': '''Actualza la glosa cuando se crea un asiento de diferencia de cambio (modelo account.move) al realizar el pago de una factura,
    o también al ejecutar los procesos de Diferencia de Cambio y de Conversión''',
	'author': 'Alvpercon',
	'website': 'https://www.alvpercon.com',
	'depends': ['account','solse_target_move'],
	'data': [
		#"security/ir.model.access.csv",
		#'views/account_move_view.xml',
	],
	'installable': True,
	'sequence': 1,
}