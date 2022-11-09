# -*- coding: utf-8 -*-
# Copyright (c) 2019-2022 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php

{
	'name': "Web Publica CPE",

	'summary': """
		Web publica para consultar los comprobantes""",

	'description': """
		Facturación electrónica - Perú 
		Web publica para consultar los comprobantes
	""",

	'author': "F & M Solutions Service S.A.C",
	'website': "http://www.solse.pe",
    'license': 'LGPL-3',
	'category': 'Website',
	'version': '15.0.1.0',
	'depends': [
		'website',
		'account',
		'solse_pe_edi',
		'solse_pe_cpe',
	],
	'data': [
		'security/solse_pe_cpe_public_security.xml',
		'security/ir.model.access.csv',
		'views/busqueda_cpe_template.xml',
	],
	'installable': True,
	'price': 15,
	'currency': 'USD',
}