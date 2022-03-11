# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning
import logging
_logging = logging.getLogger(__name__)

class Pertner(models.Model):
	_inherit = "res.partner"

	property_account_payable_2_id = fields.Many2one('account.account', company_dependent=True,
        string="Cuenta a pagar (Moneda Extranjera)",
        domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="This account will be used instead of the default one as the payable account for the current partner",
        required=True)

	@api.onchange('property_account_payable_id')
	def _onchange_receivable_id(self):
		if self.property_account_payable_id and not self.property_account_payable_2_id:
			self.property_account_payable_2_id = self.property_account_payable_id.id