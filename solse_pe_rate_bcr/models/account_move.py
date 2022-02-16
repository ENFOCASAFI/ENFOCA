# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError, Warning
import logging
_logging = logging.getLogger(__name__)

class AccountMove(models.Model):
	_inherit = 'account.move'

	#tipo_cambio = fields.Monetary('Tipo de cambio', compute="_compute_tipo_cambio", currency_field='company_currency_id')
	tipo_cambio = fields.Float('Tipo de cambio', compute="_compute_tipo_cambio", digits=(12,3))
	
	#@api.depends('currency_id', 'date', 'company_id')
	@api.depends('date', 'company_id')
	def _compute_tipo_cambio(self):
		for reg in self:
			if not reg.date or not reg.currency_id or not reg.company_id:
				reg.tipo_cambio = 1
				continue
			currency_rate_id = [
				('name','=',str(reg.date)),
				('company_id','=',reg.company_id.id),
				#('currency_id','=',reg.currency_id.id),
				('currency_id','=',2),
			]
			currency_rate_id = self.env['res.currency.rate'].sudo().search(currency_rate_id)
			if currency_rate_id:
				reg.tipo_cambio = currency_rate_id.rate_pe
			else:
				reg.tipo_cambio = 1

