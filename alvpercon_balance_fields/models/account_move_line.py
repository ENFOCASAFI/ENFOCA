# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'

	account_for_balance = fields.Integer('Cuentas seleccionadas')
	account_saldo_ini = fields.Char('Cuentas Saldo Inicial')
	account_for_balance_comp = fields.Integer('Cuentas seleccionadas comparativo')
	account_filtered_comp = fields.Char('Cuentas filtradas en comparativo')




