# -*- coding: utf-8 -*-
# Copyright (c) 2019-2020 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
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

	'category': 'Uncategorized',
	'version': '0.1',

	'depends': [
		'account',
	],
	'data': [
		'data/tareas_auxiliares.xml',
		'views/account_account.xml',
		'views/account_move_view.xml',
	],
	'auto_install': False,
	'installable': True,
	'application': True,
	"sequence": 1,
}