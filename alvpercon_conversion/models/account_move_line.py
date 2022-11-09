# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError, Warning, ValidationError
import logging
_logging = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'

	currency_multirate_affected = fields.Boolean(string='Ejecuta Diferencia Cambio' , compute="_compute_exchange_difference" ) 
	currency_multirate_affected_s = fields.Boolean(string='Ejecuta Dif Cambio' , related="currency_multirate_affected" , store=True ) # se crea porque como campo compute no almacena bien la información
	currency_multirate_conversion_affected = fields.Boolean(string='Ejecuta Diferencia Conversion' , compute="_compute_conversion_difference" )
	currency_multirate_conversion_affected_s = fields.Boolean(string='Ejecuta Dif Conversion' , related="currency_multirate_conversion_affected" , store=True )
 
	#@api.depends('currency_multirate_affected')
	def _compute_exchange_difference(self):
		for reg in self:
			
			account_id = [
					('code','=',str(reg.account_id.code)),
					('company_id','=',reg.company_id.id),
				
			]
			currency_rate_id = self.env['account.account'].sudo().search(account_id)
			reg.currency_multirate_affected_s = False
			if currency_rate_id:
				if reg.account_id.id == currency_rate_id.id:
					reg.currency_multirate_affected = currency_rate_id.currency_multirate_affected
					reg.currency_multirate_affected_s = currency_rate_id.currency_multirate_affected
			# 	else:
			# 		reg.currency_multirate_affected = False
					
			# else:
			# 	reg.currency_multirate_affected = False
			
	#@api.depends('currency_multirate_conversion_affected') 
	def _compute_conversion_difference(self):
		for reg in self:
			#pass
			account_cd_id = [
					('code','=',str(reg.account_id.code)),
					('company_id','=',reg.company_id.id),
				
			]
			currency_rate_id = self.env['account.account'].sudo().search(account_cd_id)
			reg.currency_multirate_conversion_affected = False
			if currency_rate_id:
				if reg.account_id.id == currency_rate_id.id:
					reg.currency_multirate_conversion_affected = currency_rate_id.currency_multirate_conversion_affected
					reg.currency_multirate_conversion_affected_s = currency_rate_id.currency_multirate_conversion_affected
   			# 	else:
			# 		reg.currency_multirate_conversion_affected = False
			
			# else:
			# 	reg.currency_multirate_conversion_affected = False
				
	