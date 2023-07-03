# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
	_inherit = 'account.move'

	bank_statement_ref = fields.Char(string='Reference bank', related="statement_line_id.payment_ref", store=True)
	glosa = fields.Char(string="Glosa")
	
	# se ejecuta cuando se agtega un nuevo registro en la tabla o modelo account.move
	# @api.model
	# def create(self, values) :
	# 	res = super().create(values)
	# 	query ="UPDATE account_move set glosa = bank_statement_ref  where bank_statement_ref IS NOT NULL "
	# 	self.env.cr.execute(query)
	# 	return res
	
	# se ejecuta cuando se realiza algun cambio en la tabla o modelo account.move
	def write(self, values) :
		res = super().write(values)
		query ="UPDATE account_move set glosa = bank_statement_ref  where (bank_statement_ref IS NOT NULL and glosa IS NULL) or (glosa !=bank_statement_ref) "
		self.env.cr.execute(query)
		return res	
	
	
	def updete_glosa(self) :
		pass
		# query ="UPDATE account_move set glosa = bank_statement_ref  where bank_statement_ref IS NOT NULL "
		# self.env.cr.execute(query)

		
	# @api.onchange('date')	
	# def _onchange_date_glosa(self):
	# 	for rec in self:			
	# 		if rec.date:
	# 			rec.glosa = rec.bank_statement_ref