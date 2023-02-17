# -*- coding: utf-8 -*-

{
	'name': 'Filtro de documentos en facturas',
	'version': '15.0.1.0.0',
	'category': 'Extra Tools',
	'summary': '''Módulo que agrega un campo many2many para filtrar los diario en tipos de documentos ,
	muestra solo los diarios ya sea de compra o venta, la combinación de seleccionar los diarios con el tipo de documento
	sirve para filtrar los tipos de documentos en las facturas ''',
	'author': 'Alvpercon',
	'website': 'https://www.alvpercon.com',
	'license': 'LGPL-3',
	'depends': ['base','solse_pe_edi'],
	'data': [
		#"security/ir.model.access.csv",
		#'views/account_move_view.xml',
		'views/l10n_latam_document_type_view.xml',
	],
	'installable': True,
	'sequence': 1,
}