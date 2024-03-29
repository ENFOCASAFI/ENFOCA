# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo import tools

class BalanceRecordGroupDolar(models.Model):
	_name = 'balance.record.group.dolar'
	#_auto = False
	_description = 'Campos para reporte de balance en Dólares'

	account = fields.Char('Cuenta Contables')
	name = fields.Char('Descripción')
	account_type = fields.Char('tipo de cuenta')
	account_digit = fields.Char('Digito de cuenta')
	account_digitd = fields.Char('Digito de la cuenta')
	credit_amount = fields.Float('Credito')
	debit_amount = fields.Float('Debito')
	deudor = fields.Float('Deudor')
	acreedor = fields.Float('Acreedor')
	activo = fields.Float('Activo')
	pasivo = fields.Float('Pasivo')
	perdida = fields.Float('Pérdida_N')
	ganancia = fields.Float('Ganancia_N')
	perdidan = fields.Float('Pérdida N')
	ganancian = fields.Float('Ganancia N')

	# def init(self):
	# 	tools.drop_view_if_exists(self._cr, 'balance_record_group')
	# 	self._cr.execute("""
    #         CREATE OR REPLACE VIEW balance_record_group AS (
              
	# 			SELECT
    #                 row_number() OVER () AS id,
	# 				line.account,
	# 				line.name,
	# 				line.account_type,
	# 				line.account_digit,
	# 				line.account_digitd,
    #                 line.credit_amount,
	# 				line.debit_amount,
    #                 line.deudor,
	# 				line.acreedor,
	# 				line.activo,
	# 				line.pasivo,
	# 				line.perdida,
	# 				line.ganancia,
	# 				line.perdidan,
	# 				line.ganancian       
	# 			FROM (                        
	# 					SELECT 
	# 						b.code as account,
	# 						b.name as name,
	# 						b.internal_group as account_type,
	# 						substring(b.code, 1, 1) as account_digit,
	# 						CASE WHEN substring(b.code, 1, 2) = '79' THEN substring(b.code, 1, 2) ELSE substring(b.code, 1, 1) END as account_digitd,
	# 						sum(a.debid_d) as credit_amount,
	# 						sum(a.credit_d) as debit_amount,
	# 						CASE WHEN sum(a.debid_d)-sum(a.credit_d) > 0 THEN sum(a.debid_d)-sum(a.credit_d) ELSE 0 END as deudor,
	# 						CASE WHEN sum(a.debid_d)-sum(a.credit_d) < 0 THEN (sum(a.debid_d)-sum(a.credit_d))*(-1) ELSE 0 END as acreedor,
	# 						CASE WHEN substring(b.code, 1, 1) in ('1','2','3','4','5') THEN (CASE WHEN sum(a.debid_d)-sum(a.credit_d) > 0 THEN sum(a.debid_d)-sum(a.credit_d) ELSE 0 END) ELSE 0 END as activo,
	# 						CASE WHEN substring(b.code, 1, 1) in ('1','2','3','4','5') THEN (CASE WHEN sum(a.debid_d)-sum(a.credit_d) < 0 THEN (sum(a.debid_d)-sum(a.credit_d))*(-1) ELSE 0 END) ELSE 0 END as pasivo,
	# 						CASE WHEN (CASE WHEN substring(b.code, 1, 2) = '79' THEN substring(b.code, 1, 2) ELSE substring(b.code, 1, 1) END) in ('6','7','8') THEN (CASE WHEN sum(a.debid_d)-sum(a.credit_d) > 0 THEN sum(a.debid_d)-sum(a.credit_d) ELSE 0 END) ELSE 0 END as perdida,
	# 						CASE WHEN (CASE WHEN substring(b.code, 1, 2) = '79' THEN substring(b.code, 1, 2) ELSE substring(b.code, 1, 1) END) in ('7') THEN (CASE WHEN sum(a.debid_d)-sum(a.credit_d) < 0 THEN (sum(a.debid_d)-sum(a.credit_d))*(-1) ELSE 0 END) ELSE 0 END as ganancia,
	# 						CASE WHEN (CASE WHEN substring(b.code, 1, 2) = '79' THEN substring(b.code, 1, 2) ELSE substring(b.code, 1, 1) END) in ('8','9') THEN (CASE WHEN sum(a.debid_d)-sum(a.credit_d) > 0 THEN sum(a.debid_d)-sum(a.credit_d) ELSE 0 END) ELSE 0 END as perdidan,
	# 						CASE WHEN (CASE WHEN substring(b.code, 1, 2) = '79' THEN substring(b.code, 1, 2) ELSE substring(b.code, 1, 1) END) in ('7') THEN (CASE WHEN sum(a.debid_d)-sum(a.credit_d) < 0 THEN (sum(a.debid_d)-sum(a.credit_d))*(-1) ELSE 0 END) ELSE 0 END as ganancian
	# 					FROM 
	# 						account_move_line a 
	# 					 LEFT JOIN 
	# 					 	account_account b
	# 					 ON 
	# 					 	a.account_id = b.id
	# 					 WHERE 
	# 					 	a.account_for_balance = 1 AND a.parent_state = 'posted' 
	# 					GROUP BY
	# 						a.account_id,
	# 						b.code,
	# 						b.name,
	# 						b.internal_group,
	# 						substring(b.code, 1, 1),
	# 						CASE WHEN substring(b.code, 1, 2) = '79' THEN substring(b.code, 1, 2) ELSE substring(b.code, 1, 1) END 
	# 					ORDER BY
	# 						b.code						

    #                   ) as line
			     
    #         )""")



