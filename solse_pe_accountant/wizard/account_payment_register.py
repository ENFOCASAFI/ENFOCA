# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logging = logging.getLogger(__name__)

class AccountPaymentRegister(models.TransientModel):
	_inherit = 'account.payment.register'

	es_detraccion_retencion = fields.Boolean("Es por Detracción/Retención", help="Marcar si el pago es por la detracción o retención")


	@api.depends('can_edit_wizard')
	def _compute_communication(self):
		for wizard in self:
			if wizard.can_edit_wizard:
				batches = wizard._get_batches()
				dato = wizard._get_batch_communication(batches[0])
				partes = dato.split(" ")
				dato = dato if len(partes) == 1 else dato[1]
				wizard.communication = dato
			else:
				wizard.communication = False

	@api.model
	def _get_wizard_values_from_batch(self, batch_result):
		key_values = batch_result['key_values']
		lines = batch_result['lines']
		company = lines[0].company_id
		factura = lines[0].move_id

		source_amount = abs(sum(lines.mapped('amount_residual')))
		source_amount = source_amount - factura.monto_detraccion - factura.monto_retencion
		if key_values['currency_id'] == company.currency_id.id:
			source_amount_currency = source_amount
		else:
			source_amount_currency = abs(sum(lines.mapped('amount_residual_currency')))
			source_amount_currency = source_amount_currency - factura.monto_detraccion_base - factura.monto_retencion_base

		return {
			'company_id': company.id,
			'partner_id': key_values['partner_id'],
			'partner_type': key_values['partner_type'],
			'payment_type': key_values['payment_type'],
			'source_currency_id': key_values['currency_id'],
			'source_amount': source_amount,
			'source_amount_currency': source_amount_currency,
		}

	@api.onchange('es_detraccion_retencion')
	def _onchange_detraccion_retencion(self):
		factura = self.line_ids[0].move_id
		self.payment_difference_handling = "open"
		if factura.company_id.currency_id.id == self.currency_id.id:
			if self.es_detraccion_retencion:
				self.amount = factura.monto_detraccion + factura.monto_retencion
			else:
				source_amount = abs(factura.amount_residual)
				self.amount = source_amount - factura.monto_detraccion - factura.monto_retencion
		else:
			if self.es_detraccion_retencion:
				self.amount = factura.monto_detraccion_base + factura.monto_retencion_base
			else:
				amount_residual_currency = abs(factura.amount_residual_currency)
				self.amount = amount_residual_currency - factura.monto_detraccion_base - factura.monto_retencion_base
