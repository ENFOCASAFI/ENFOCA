# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError, Warning, ValidationError
import logging
_logging = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'

	target_accountb = fields.Boolean(string='Tiene cuenta de destino' , compute="_compute_target_account" ) 
	target_account_b = fields.Boolean(string='Tiene cuenta de destino.' , related="target_accountb" , store=True ) # se crea porque como campo compute no almacena bien la información
	
	def _compute_target_account(self):
		for reg in self:
			# pass
			account_id = [
					('code','=',str(reg.account_id.code)),
					('company_id','=',reg.company_id.id),
				
			]
			currency_rate_id = self.env['account.account'].sudo().search(account_id)
			# reg.target_account_b = True
			if currency_rate_id:
				if reg.account_id.id == currency_rate_id.id:
					reg.target_accountb = currency_rate_id.target_account
					reg.target_account_b = currency_rate_id.target_account # SE AGREGA PORQUE NO SE ACTUALIZA Y SE TIENE QUE REFRESCAR DOS VECES PARA VER EL CAMBIO
	