# -*- coding: utf-8 -*-
# Copyright (c) 2019-2023 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

{
	'name': "Asientos de destino",

	'summary': """
		Asientos de destino""",

	'description': """
		Asientos de destino
	""",

	'author': "F & M Solutions Service S.A.C",
	'website': "http://www.solse.pe",

	'category': 'Financial',
	'version': '15.1.0.6',
	'license': 'LGPL-3',
	'depends': [
		'account',
		'solse_pe_accountant',
	],
	'data': [
		'security/ir.model.access.csv',
		'data/tareas_auxiliares.xml',
		'wizard/agregar_movimientos_destino.xml',
		'views/account_account.xml',
		'views/account_move_view.xml',
	],
	'auto_install': False,
	'installable': True,
	'application': True,
	"sequence": 1,
}