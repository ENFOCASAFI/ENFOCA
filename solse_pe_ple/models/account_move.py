# -*- coding: utf-8 -*-
# Copyright (c) 2019-2020 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
import logging
_logging = logging.getLogger(__name__)

class AccountMove(models.Model) :
	_inherit = 'account.move'

	pago_detraccion = fields.Many2one('account.payment', 'Pago de Detracción/Retención')

	"""def obtener_total_base_afecto(self):
		suma = 0
		for linea in self.invoice_line_ids:
			if linea.pe_affectation_code in ('10', '11', '12', '13', '14', '15', '16'):
				suma = suma + abs(linea.balance)
		return suma

	def obtener_total_base_inafecto(self):
		suma = 0
		for linea in self.invoice_line_ids:
			if linea.pe_affectation_code not in ('10', '11', '12', '13', '14', '15', '16'):
				suma = suma + abs(linea.balance)
		return suma"""

	
	def obtener_valor_campo_14(self, tipo_cambio):
		suma = 0
		for linea in self.invoice_line_ids:
			if linea.tipo_afectacion_compra.nro_col_importe_afectacion == 14:
				monto = abs(linea.price_subtotal)
				monto = monto * tipo_cambio
				suma = suma + monto

		respuesta = ""
		if suma > 0:
			respuesta = format(suma, '.2f')
		else:
			respuesta = ""

		return respuesta

	def obtener_valor_campo_15(self, tipo_cambio):
		suma = 0
		for linea in self.invoice_line_ids:
			impuesto_afect_ids = []
			if not linea.tax_ids:
				raise UserError("La factura %s no contiene impuestos en su linea %s" % (linea.move_id.name, linea.name))
			impuesto = linea.tax_ids[0]
			for item in linea.tipo_afectacion_compra.impuesto_afect_ids:
				if impuesto.id == item.impuesto_id.id and item.nro_col_importe_impuesto == 15:
					monto = abs(linea.price_total - linea.price_subtotal)
					monto = monto * tipo_cambio
					suma = suma + monto

		respuesta = ""
		if suma > 0:
			respuesta = format(suma, '.2f')
		else:
			respuesta = ""
			
		return respuesta

	def obtener_valor_campo_16(self, tipo_cambio):
		suma = 0
		for linea in self.invoice_line_ids:
			if linea.tipo_afectacion_compra.nro_col_importe_afectacion == 16:
				monto = abs(linea.price_subtotal)
				monto = monto * tipo_cambio
				suma = suma + monto

		respuesta = ""
		if suma > 0:
			respuesta = format(suma, '.2f')
		else:
			respuesta = ""

		return respuesta

	def obtener_valor_campo_17(self, tipo_cambio):
		suma = 0
		for linea in self.invoice_line_ids:
			impuesto_afect_ids = []
			impuesto = linea.tax_ids[0]
			for item in linea.tipo_afectacion_compra.impuesto_afect_ids:
				if impuesto.id == item.impuesto_id.id and item.nro_col_importe_impuesto == 17:
					monto = abs(linea.price_total - linea.price_subtotal)
					monto = monto * tipo_cambio
					suma = suma + monto

		respuesta = ""
		if suma > 0:
			respuesta = format(suma, '.2f')
		else:
			respuesta = ""
			
		return respuesta

	def obtener_valor_campo_18(self, tipo_cambio):
		suma = 0
		for linea in self.invoice_line_ids:
			if linea.tipo_afectacion_compra.nro_col_importe_afectacion == 18:
				monto = abs(linea.price_subtotal)
				monto = monto * tipo_cambio
				suma = suma + monto

		respuesta = ""
		if suma > 0:
			respuesta = format(suma, '.2f')
		else:
			respuesta = ""

		return respuesta

	def obtener_valor_campo_19(self, tipo_cambio):
		suma = 0
		for linea in self.invoice_line_ids:
			impuesto_afect_ids = []
			impuesto = linea.tax_ids[0]
			for item in linea.tipo_afectacion_compra.impuesto_afect_ids:
				if impuesto.id == item.impuesto_id.id and item.nro_col_importe_impuesto == 19:
					monto = abs(linea.price_total - linea.price_subtotal)
					monto = monto * tipo_cambio
					suma = suma + monto

		respuesta = ""
		if suma > 0:
			respuesta = format(suma, '.2f')
		else:
			respuesta = ""
			
		return respuesta

	def obtener_valor_campo_20(self, tipo_cambio):
		suma = 0
		for linea in self.invoice_line_ids:
			if linea.tipo_afectacion_compra.nro_col_importe_afectacion == 20:
				monto = abs(linea.price_subtotal)
				monto = monto * tipo_cambio
				suma = suma + monto

		respuesta = ""
		if suma > 0:
			respuesta = format(suma, '.2f')
		else:
			respuesta = ""

		return respuesta

	def obtener_valor_campo_21(self, tipo_cambio):
		suma = 0
		for linea in self.invoice_line_ids:
			impuesto_afect_ids = []
			impuesto = linea.tax_ids[0]
			for item in linea.tipo_afectacion_compra.impuesto_afect_ids:
				if impuesto.id == item.impuesto_id.id and item.nro_col_importe_impuesto == 21:
					monto = abs(linea.price_total - linea.price_subtotal)
					monto = monto * tipo_cambio
					suma = suma + monto

		respuesta = ""
		if suma > 0:
			respuesta = format(suma, '.2f')
		else:
			respuesta = ""
			
		return respuesta

	def obtener_valor_campo_22(self, tipo_cambio):
		suma = 0
		for linea in self.invoice_line_ids:
			impuesto_afect_ids = []
			impuesto = linea.tax_ids[0]
			for item in linea.tipo_afectacion_compra.impuesto_afect_ids:
				if impuesto.id == item.impuesto_id.id and item.nro_col_importe_impuesto == 22:
					monto = abs(linea.price_total - linea.price_subtotal)
					monto = monto * tipo_cambio
					suma = suma + monto

		respuesta = ""
		if suma > 0:
			respuesta = format(suma, '.2f')
		else:
			respuesta = ""
			
		return respuesta

	def obtener_valor_campo_23(self, tipo_cambio):
		suma = 0
		for linea in self.invoice_line_ids:
			if linea.tipo_afectacion_compra.nro_col_importe_afectacion == 23:
				monto = abs(linea.price_subtotal)
				monto = monto * tipo_cambio
				suma = suma + monto

		respuesta = ""
		if suma > 0:
			respuesta = format(suma, '.2f')
		else:
			respuesta = ""

		return respuesta

	def obtener_valor_campo_24(self, tipo_cambio):
		suma = 0
		for linea in self.invoice_line_ids:
			suma = suma + abs(linea.balance)

		respuesta = ""
		if suma > 0:
			respuesta = format(suma, '.2f')
		else:
			respuesta = ""
			
		return respuesta

class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'

	glosa = fields.Char("Glosa", related="move_id.glosa", store=True)
