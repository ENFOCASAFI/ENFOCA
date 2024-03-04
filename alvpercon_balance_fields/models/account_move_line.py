# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'

	account_for_balance = fields.Integer('Cuentas seleccionadas')
	




