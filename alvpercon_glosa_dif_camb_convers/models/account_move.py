# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
	_inherit = 'account.move'

	glosa_relacionada = fields.Char(string='Glosa relacionada', compute="_compute_glosa" , readonly=False ,store=True)

	@api.depends('glosa')
	def _compute_glosa(self):
		## Tabla1 --> selecciona los registros que tenen glosa de proceso de diferencia de cambio
		account_id = [
					('glosa','!=',False),
					('is_exchange_difference_process_move','=',True),			
			]
		currency_rate_id = self.env['account.move'].sudo().search(account_id)
		#print("Reg dif camb...", currency_rate_id)
		## Tabla2 --> selecciona los registros que tenen glosa de proceso de Conversión
		account_ids = [
					('glosa','!=',False),
					('is_conversion_process_move','=',True),					
			]
		currency_rate1_id = self.env['account.move'].sudo().search(account_ids)
		#print("Reg conv...",currency_rate1_id)
		
		## Tabla3 --> selecciona los registros que no tienen glosa
		account2_id = [
					('glosa','=',False)					
			]
		currency_rate2_id = self.env['account.move'].sudo().search(account2_id)
		
		#print("Reg sin Glosa...",currency_rate2_id)
		#Relaciona la tabla 1 y 3 por las id de origen para actualizar la Glosa.
		for reg in currency_rate_id:						
			if reg:
				
				for reg2 in currency_rate2_id:
					if reg2:
						#print("id reg df",reg.id)						
						#print("id reg ",reg2.id)
						#print("Reg Origen Dif Camb",reg2.origin_move_id)
						if reg2.origin_move_id.id == reg.id:
							reg2.glosa_relacionada = reg.glosa
							#print("Reg Con Glosa", reg.glosa)
							#print("Glosa Actulizada", reg2.glosa)
		#Relaciona la tabla 2 y 3 por las id de origen para actualizar la Glosa.
		for reg1 in currency_rate1_id:						
			if reg1:
				
				for reg3 in currency_rate2_id:
					if reg3:
						#print("id reg c",reg1.id)						
						#print("id reg ",reg3.id)
						#print("Reg Origen Conv",reg3.origin_move_id)
						if reg3.origin_move_id.id == reg1.id:
							reg3.glosa_relacionada = reg1.glosa
							#print("Reg Con Glosa", reg1.glosa)
							#print("Glosa Actulizada", reg3.glosa)


	
	def write(self, values) :
		res = super().write(values)
        # account_payment.glosa
		query ="UPDATE account_move SET glosa = 'Diferencia de Cambio' FROM account_payment WHERE account_move.create_date = account_payment.create_date and account_move.glosa is null; "
		self.env.cr.execute(query)

		# query1 = "UPDATE account_move SET glosa = ref WHERE glosa is null;"
		query1 = "UPDATE account_move SET glosa = 'Ajuste por Diferencia de Cambio' WHERE is_exchange_difference_process_move = 't' and glosa IS NULL;"
		self.env.cr.execute(query1)

		query2 = "UPDATE account_move SET glosa = 'Ajuste por Conversión' WHERE is_conversion_process_move = 't' and glosa IS NULL;"
		self.env.cr.execute(query2)
		
		query2 = "UPDATE account_move SET glosa = glosa_relacionada WHERE glosa_relacionada is not null and glosa is null;"
		self.env.cr.execute(query2)
		
		
		return res
		
	
		
	
class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'

	def write(self, values) :
		res = super().write(values)
		query ="UPDATE account_move_line SET glosa = account_move.glosa FROM account_move WHERE account_move.id = account_move_line.move_id and account_move.glosa is not null and account_move_line.glosa is null; "
		self.env.cr.execute(query)
		return res


	