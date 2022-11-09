# -*- coding: utf-8 -*-
# Copyright (c) 2021 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError, Warning, ValidationError
import xml.etree.cElementTree as ET
from lxml import etree
import json
import logging
from . import constantes
_logging = logging.getLogger(__name__)


class PeDatas(models.Model):
	_inherit = 'pe.datas'

	@api.model
	def get_selection_description(self, table_code):
		res=[]
		datas=self.search([('table_code', '=', table_code)])
		if datas:
			res = [(data.code, data.description) for data in datas]
		return res



class LineaAfectacionCompra(models.Model):
	_name = "solse.pe.afectacion.compra"
	_description = "Linea Afectación compra"

	name = fields.Char("Nombre")
	active = fields.Boolean(default=True)
	sequence = fields.Integer(default=10)
	impuesto_afect_ids = fields.One2many(comodel_name="solse.pe.impuesto.afectacion.compra", inverse_name="linea_afectacion_id", string="Impuesto")
	impuesto_defecto = fields.Many2one("solse.pe.impuesto.afectacion.compra", domain="[('id', 'in', impuesto_afect_ids)]", string="Impuesto por defecto")
	nro_col_importe_afectacion = fields.Integer("Columna Importe Afectación")

class ImpuestoAfectacionCompra(models.Model):
	_name = "solse.pe.impuesto.afectacion.compra"
	_description = "Impuesto Afectación compra"

	active = fields.Boolean(default=True)
	linea_afectacion_id = fields.Many2one("solse.pe.afectacion.compra", string="Afectación compra")
	impuesto_id = fields.Many2one("account.tax", string="Impuesto")
	name = fields.Char("Nombre", related="impuesto_id.name")
	nro_col_importe_impuesto = fields.Integer("Columna Importe Impuesto")
	

class AccountMove(models.Model):
	_inherit = 'account.move'

	@api.model
	def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
		res = super(AccountMove, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
		if view_type in ['form']:
			paso_validacion = False
			if self._context.get('params') and 'action' in self._context['params']:
				parametros = self._context['params']
				accion = self.env['ir.actions.act_window'].search([('id', '=', parametros['action'])])
				if accion and accion.domain and ('in_invoice' in accion.domain or 'in_refund' in accion.domain):
					paso_validacion = True

			elif self._context.get('default_move_type'):
				move_type = self._context.get('default_move_type')
				if move_type in ['in_invoice', 'in_refund']:
					paso_validacion = True

			#{'action': 198, 'cids': 1, 'id': '', 'menu_id': 101, 'model': 'account.move', 'view_type': 'form'}
			if paso_validacion:
				str_productos_ter_cant = res['fields']['invoice_line_ids']['views']['tree']['arch']
				root_temp = ET.fromstring(str_productos_ter_cant)
				t2 = ET.tostring(root_temp, encoding='utf8', method='xml')
				xml_productos_ter_cant = etree.XML(t2)
				node = xml_productos_ter_cant.xpath("//field[@name='tipo_afectacion_compra']")[0]
				node.set('invisible', '0')
				node.set('force_save', '1')
				json_mod = {
					'column_invisible': False,
				}
				node.set("modifiers", json.dumps(json_mod))
				respuesta = ET.tostring(xml_productos_ter_cant, encoding='utf-8', method='xml')
				res['fields']['invoice_line_ids']['views']['tree']['arch'] = respuesta

		return res

DATOS_AFECTACION_COMPRA = [
	('1014', 'B. Imp. Adq. Grav. Créd. Fiscal y/o Saldo favor Export., dest. exclus. Operac. Grav. y/o de Export.'),
	('1015', 'IGV y/o IPM'),
	('1016', 'B. Imp. Adq. Grav. Créd. Fiscal y/o Saldo favor Export., dest. Operac. Grav. y/o de Export. y Operac. NO Grav.'),
	('1017', 'IGV y/o IPM'),
	('1018', 'B. Imp. Adq. Grav. NO Créd. Fiscal y/o Saldo favor Export., NO dest. Operac. Grav. y/o de Export.'),
	('1019', 'IGV y/o IPM'),
	('1020', 'Adquisic. NO Grav.'),
	('1021', 'ISC'),
	('1022', 'ICBPER'),
	('1023', 'Otros conceptos, tributos y cargos NO forman parte de la B. Imponib.')
]

class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'

	def _default_afectacion_compra(self):
		afectacion = self.env['solse.pe.afectacion.compra'].search([], limit=1)

		return afectacion

	tipo_afectacion_fact_compra = fields.Selection(selection=DATOS_AFECTACION_COMPRA, string='Tipo de afectación', default='1015', help='Tipo de afectación Compra', store=True)
	tipo_afectacion_compra = fields.Many2one("solse.pe.afectacion.compra", string='Tipo de afectación', help='Tipo de afectación Compra', store=True)

	@api.onchange('tipo_afectacion_compra')
	def onchange_tipo_afectacion_compra(self):
		if not self.move_id.move_type in ['in_invoice', 'in_refund']:
			return


		if self.tipo_afectacion_compra:
			"""ids = self.tax_ids.filtered(lambda tax: tax.l10n_pe_edi_tax_code == constantes.IMPUESTO['igv'] and tax.type_tax_use == 'purchase').ids
			res = self.env['account.tax'].search([('l10n_pe_edi_tax_code', '=', constantes.IMPUESTO['igv']), ('id', 'in', ids)])
			if not res:
				res = self.env['account.tax'].search([('l10n_pe_edi_tax_code', '=', constantes.IMPUESTO['igv']), ('type_tax_use', '=', 'purchase')], limit=1)
			"""
			por_defecto = False
			impuesto = self.tax_ids[0]
			impuesto_afect_ids = []

			for item in self.tipo_afectacion_compra.impuesto_afect_ids:
				impuesto_afect_ids.append(item.impuesto_id.id)

			if impuesto._origin.id in impuesto_afect_ids:
				return

			if self.tipo_afectacion_compra.impuesto_defecto and self.tipo_afectacion_compra.impuesto_defecto.impuesto_id:
				por_defecto = self.tipo_afectacion_compra.impuesto_defecto.impuesto_id.id

			if not por_defecto and self.tipo_afectacion_compra.impuesto_afect_ids:
				por_defecto = self.tipo_afectacion_compra.impuesto_afect_ids[0].impuesto_id.id

			if por_defecto:
				self.tax_ids = [(6, 0, [por_defecto])]

			self._set_free_tax_purchase()

	def set_pe_affectation_purchase_code(self):
		if self.tax_ids:
			impuesto = self.tax_ids[0]
			impuesto_afect_ids = []
			for item in self.tipo_afectacion_compra.impuesto_afect_ids:
				impuesto_afect_ids.append(item.impuesto_id.id)

			if impuesto._origin.id in impuesto_afect_ids:
				return

			afectacion_compra_ids = self.env['solse.pe.afectacion.compra'].search([])
			for afectacion in afectacion_compra_ids:
				impuesto_afect_ids = []
				for item in afectacion.impuesto_afect_ids:
					impuesto_afect_ids.append(item.impuesto_id.id)

				if impuesto._origin.id in impuesto_afect_ids:
					self.tipo_afectacion_compra = afectacion.id

	@api.onchange('tax_ids')
	def _onchange_impuesto_compra(self):
		if self.tax_ids:
			impuesto = self.tax_ids[0]
			impuesto_afect_ids = []
			for item in self.tipo_afectacion_compra.impuesto_afect_ids:
				impuesto_afect_ids.append(item.impuesto_id.id)

			if impuesto._origin.id in impuesto_afect_ids:
				return

			afectacion_compra_ids = self.env['solse.pe.afectacion.compra'].search([])
			for afectacion in afectacion_compra_ids:
				impuesto_afect_ids = []
				for item in afectacion.impuesto_afect_ids:
					impuesto_afect_ids.append(item.impuesto_id.id)

				if impuesto._origin.id in impuesto_afect_ids:
					self.tipo_afectacion_compra = afectacion.id
					return

	@api.onchange('product_id')
	def _onchange_purchase_product_id(self):
		for rec in self.filtered(lambda x: x.product_id):
			rec.set_pe_affectation_purchase_code()

		self = self.with_context(check_move_validity=False)


	def _set_free_tax_purchase(self):
		return
		if self.tipo_afectacion_fact_compra in ('9996'):
			self.discount = 100
		else:
			if self.discount == 100:
				self.discount = 0

		
 
		


