# -*- coding: utf-8 -*-
# Copyright (c) 2021 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

{
	'name': 'Perú - Telecrédito',
	'version': '15.1.0.0',
	'category': 'Financial',
	'summary': 'Perú - Telecrédito',
    'website': 'https://www.alvpercon.com',
	'license': 'LGPL-3',
	'depends': [
		'solse_pe_edi',
		'solse_pe_cpe',
	],
	'data': [
		'security/ir.model.access.csv',
		'views/telecredito_view.xml',
		'views/res_partner_view.xml',
		'wizard/pago_telecredito_view.xml',
	],
	'license': 'Other proprietary',
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
