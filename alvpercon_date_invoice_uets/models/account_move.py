# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
	_inherit = 'account.move'

	def write(self, values) :
		res = super().write(values)
		for rec in self:
			if rec.date and rec.invoice_date:
				if rec.date < rec.invoice_date:
					raise ValidationError(_("La FECHA CONTABLE que ha registrado es menor a la fecha de la FACTURA verifique si es correcto o no."))

		return res
	
	# @api.onchange('date')
	# def _onchange_date(self):
	# 	for rec in self:
	# 		if rec.date and rec.invoice_date:
	# 			if rec.date < rec.invoice_date:
	# 				raise ValidationError(_("La FECHA CONTABLE que ha registrado es menor a la fecha de la FACTURA verifique si es correcto o no."))

		