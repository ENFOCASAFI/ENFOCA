# -*- coding: utf-8 -*-

{
	'name': 'Campos origen de diarios por función',
	'version': '15.0.1.0.0',
	'category': 'Extra Tools',
	'summary': '''Muestra en el Formulario "Asientos contables" y en la vista tree "varios" dentro de contabilidad los números de origen 
	que generan los asientos de destino por función que estan ubicados en la tabla accoun.move y account.move.line
	y acount.move.le''',
	'author': 'Alvpercon',
	'website': 'https://www.alvpercon.com',
	'license': 'LGPL-3',
	'depends': ['account','solse_target_move'],
	'data': [
		#"security/ir.model.access.csv",
		'views/account_move_view.xml',
		'views/account_move_line_view.xml',
	],
	'installable': True,
	'sequence': 1,
}