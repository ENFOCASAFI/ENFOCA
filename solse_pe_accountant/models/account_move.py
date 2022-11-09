# -*- coding: utf-8 -*-
# Copyright (c) 2019-2022 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php

from odoo import models, fields, api
import logging
import datetime
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
_logging = logging.getLogger(__name__)

class AccountPayment(models.Model):
	_inherit = 'account.payment'

	transaction_number = fields.Char(string='Número de operación')
	glosa = fields.Char('Glosa', compute="_compute_glosa", store=True)

	@api.depends('reconciled_invoice_ids')
	def _compute_glosa(self):
		for reg in self:
			if not reg.reconciled_invoice_ids and not reg.reconciled_bill_ids:
				reg.glosa = ''
				continue

			factura = False
			if reg.reconciled_invoice_ids:
				factura = reg.reconciled_invoice_ids[0]
			elif reg.reconciled_bill_ids:
				factura = reg.reconciled_bill_ids[0]
				
			if not factura:
				reg.glosa = ''
				continue

			reg.glosa = factura.glosa
			reg.move_id.write({'glosa': factura.glosa})

class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'

	transaction_number = fields.Char(related='payment_id.transaction_number', store=True)
	glosa = fields.Char("Glosa", related="move_id.glosa", store=True)

class StatementLine(models.Model):
	_inherit = 'account.bank.statement.line'

	transaction_number = fields.Char(string='Número de transacción')


class AccountMove(models.Model):
	_inherit = 'account.move'

	transaction_number = fields.Char(related='payment_id.transaction_number', store=True)
	asiento_det_ret = fields.Many2one('account.move', string='Asiento retención/detracción')
	pago_detraccion = fields.Many2one('account.payment', 'Pago de Detracción/Retención', copy=False)

	es_x_apertura = fields.Boolean("Movimiento por Apertura")
	fecha_apertura = fields.Date("Fecha Apertura", default=fields.Date.context_today, readonly=True, states={'draft': [('readonly', False)]},)
	glosa = fields.Char('Glosa')
	#tipo_cambio_dolar_sistema = fields.Float("Tipo Cambio ($)", compute="_compute_tipo_cambio_sistema", store=False, digits=(16, 3))

	@api.onchange('es_x_apertura', 'fecha_apertura')
	def _onchange_fecha_apertura(self):
		if self.es_x_apertura and self.fecha_apertura:
			self.date = self.fecha_apertura or fields.Date.context_today(self)
		else:
			self.date = self.invoice_date or fields.Date.context_today(self)

	def _post(self, soft=True):
		res = super(AccountMove, self)._post()

		return res

	"""@api.depends('invoice_date', 'currency_id')
	def _compute_tipo_cambio_sistema(self):
		for reg in self:
			if reg.currency_id and reg.currency_id.name == 'USD':
				moneda_dolar = reg.currency_id
			else:
				tipo = 'venta'
				if reg.move_type in ['out_invoice', 'out_refund']:
					tipo = 'venta'
				if reg.move_type in ['in_invoice', 'in_refund']:
					tipo = 'compra'
				moneda_dolar = self.env["res.currency"].search([("name", "=", "USD"), ("rate_type", "=", tipo)], limit=1)

			if not moneda_dolar:
				moneda_dolar = self.env["res.currency"].search([("name", "=", "USD")], limit=1)

			tipo_cambio = 1.0
			if reg.invoice_date:
				tipo_cambio = moneda_dolar._convert(1.000, reg.company_id.currency_id, reg.company_id, reg.invoice_date, round=False)
			reg.tipo_cambio_dolar_sistema = tipo_cambio"""

	def obtener_totales_linea_detraccion(self, total_balance, total_amount_currency, total):
		if total_balance > 0:
			monto_detraccion = total - self.monto_neto_pagar
			#monto_detraccion = self.monto_detraccion
			total_balance_neto = total_balance - monto_detraccion
			#total_balance_detra = self.monto_detraccion
			total_balance_detra = monto_detraccion

			total_amount_currency_neto = total_amount_currency - self.monto_detraccion_base
			total_amount_currency_detra = self.monto_detraccion_base
		else:
			monto_detraccion = total - self.monto_neto_pagar
			#monto_detraccion = self.monto_neto_pagar
			total_balance_neto = total_balance + monto_detraccion
			#total_balance_detra = self.monto_detraccion * -1
			total_balance_detra = monto_detraccion * -1

			total_amount_currency_neto = total_amount_currency + self.monto_detraccion_base
			total_amount_currency_detra = self.monto_detraccion_base * -1

		respuesta = {
			'total_balance_neto': total_balance_neto,
			'total_balance_detra': total_balance_detra,
			'total_amount_currency_neto': total_amount_currency_neto,
			'total_amount_currency_detra': total_amount_currency_detra,
		}
		return respuesta

	def _recompute_payment_terms_lines(self):
		''' Compute the dynamic payment term lines of the journal entry.'''
		self.ensure_one()
		self = self.with_company(self.company_id)
		in_draft_mode = self != self._origin
		today = fields.Date.context_today(self)
		self = self.with_company(self.journal_id.company_id)

		def _get_payment_terms_computation_date(self):
			''' Get the date from invoice that will be used to compute the payment terms.
			:param self:    The current account.move record.
			:return:        A datetime.date object.
			'''
			if self.invoice_payment_term_id:
				return self.invoice_date or today
			else:
				return self.invoice_date_due or self.invoice_date or today

		def _get_payment_terms_account(self, payment_terms_lines):
			''' Get the account from invoice that will be set as receivable / payable account.
			:param self:                    The current account.move record.
			:param payment_terms_lines:     The current payment terms lines.
			:return:                        An account.account record.
			'''
			if payment_terms_lines:
				# Retrieve account from previous payment terms lines in order to allow the user to set a custom one.
				return payment_terms_lines[0].account_id
			elif self.partner_id:
				# Retrieve account from partner.
				if self.is_sale_document(include_receipts=True):
					return self.partner_id.property_account_receivable_id
				else:
					return self.partner_id.property_account_payable_id
			else:
				# Search new account.
				domain = [
					('company_id', '=', self.company_id.id),
					('internal_type', '=', 'receivable' if self.move_type in ('out_invoice', 'out_refund', 'out_receipt') else 'payable'),
				]
				return self.env['account.account'].search(domain, limit=1)

		def _compute_payment_terms(self, date, total_balance, total_amount_currency, account):
			''' Compute the payment terms.
			:param self:                    The current account.move record.
			:param date:                    The date computed by '_get_payment_terms_computation_date'.
			:param total_balance:           The invoice's total in company's currency.
			:param total_amount_currency:   The invoice's total in invoice's currency.
			:return:                        A list <to_pay_company_currency, to_pay_invoice_currency, due_date>.
			'''
			if self.invoice_payment_term_id:
				to_compute = self.invoice_payment_term_id.compute(total_balance, date_ref=date, currency=self.company_id.currency_id)
				if self.currency_id == self.company_id.currency_id:
					# Single-currency.
					if self.tiene_detraccion and self.move_type == 'in_invoice':
						datos = []
						contador = 1
						cuenta_det_id = self.env['ir.config_parameter'].sudo().get_param('solse_pe_accountant.default_cuenta_detracciones')
						cuenta_det_id = int(cuenta_det_id)
						cuenta_det = self.env['account.account'].search([('id', '=', cuenta_det_id)], limit=1)
						for b in to_compute:
							if contador == 1 and self.tiene_detraccion and self.move_type == 'in_invoice':
								contador += 1
								total_balance_local = b[1]
								totales = self.obtener_totales_linea_detraccion(b[1], b[1], total_balance)
								total_balance_neto = totales['total_balance_neto']
								total_balance_detra = totales['total_balance_detra']
								total_amount_currency_neto = totales['total_amount_currency_neto']
								total_amount_currency_detra = totales['total_amount_currency_detra']
								datos.append((fields.Date.to_string(date), total_balance_neto, total_amount_currency_neto, account))
								datos.append((fields.Date.to_string(date + datetime.timedelta(days=1)), total_balance_detra, total_amount_currency_detra, cuenta_det))
								datos.append((b[0], total_balance, b[1], account))
							else:
								datos.append((b[0], b[1], b[1], account))

					else:
						datos = [(b[0], b[1], b[1]) for b in to_compute]

					return datos
					
				else:
					# Multi-currencies.
					if self.tiene_detraccion and self.move_type == 'in_invoice':
						datos = []
						contador = 1
						cuenta_det_id = self.env['ir.config_parameter'].sudo().get_param('solse_pe_accountant.default_cuenta_detracciones')
						cuenta_det_id = int(cuenta_det_id)
						cuenta_det = self.env['account.account'].search([('id', '=', cuenta_det_id)], limit=1)
						to_compute_currency = self.invoice_payment_term_id.compute(total_amount_currency, date_ref=date, currency=self.currency_id)
						for b, ac in zip(to_compute, to_compute_currency):
							if contador == 1:
								contador += 1
								total_balance_local = b[1]
								totales = self.obtener_totales_linea_detraccion(b[1], ac[1], total_balance)
								total_balance_neto = totales['total_balance_neto']
								total_balance_detra = totales['total_balance_detra']
								total_amount_currency_neto = totales['total_amount_currency_neto']
								total_amount_currency_detra = totales['total_amount_currency_detra']
								datos.append((fields.Date.to_string(date), total_balance_neto, total_amount_currency_neto, account))
								datos.append((fields.Date.to_string(date + datetime.timedelta(days=1)), total_balance_detra, total_amount_currency_detra, cuenta_det))
							else:
								datos.append((b[0], b[1], ac[1], account))

					else:
						to_compute_currency = self.invoice_payment_term_id.compute(total_amount_currency, date_ref=date, currency=self.currency_id)
						datos = [(b[0], b[1], ac[1], account) for b, ac in zip(to_compute, to_compute_currency)]

					return datos
			else:
				if self.tiene_detraccion and self.move_type == 'in_invoice':
					datos = []
					cuenta_det_id = self.env['ir.config_parameter'].sudo().get_param('solse_pe_accountant.default_cuenta_detracciones')
					cuenta_det_id = int(cuenta_det_id)
					cuenta_det = self.env['account.account'].search([('id', '=', cuenta_det_id)], limit=1)
					totales = self.obtener_totales_linea_detraccion(total_balance, total_amount_currency, total_balance)
					total_balance_neto = totales['total_balance_neto']
					total_balance_detra = totales['total_balance_detra']
					total_amount_currency_neto = totales['total_amount_currency_neto']
					total_amount_currency_detra = totales['total_amount_currency_detra']

					"""if total_balance > 0:
						monto_detraccion = total_balance - self.monto_neto_pagar
						#monto_detraccion = self.monto_detraccion
						total_balance_neto = total_balance - monto_detraccion
						#total_balance_detra = self.monto_detraccion
						total_balance_detra = monto_detraccion

						total_amount_currency_neto = total_amount_currency - self.monto_detraccion_base
						total_amount_currency_detra = self.monto_detraccion_base
					else:
						monto_detraccion = total_balance - self.monto_neto_pagar
						#monto_detraccion = self.monto_neto_pagar
						total_balance_neto = total_balance + monto_detraccion
						#total_balance_detra = self.monto_detraccion * -1
						total_balance_detra = monto_detraccion * -1

						total_amount_currency_neto = total_amount_currency + self.monto_detraccion_base
						total_amount_currency_detra = self.monto_detraccion_base * -1"""

					datos.append((fields.Date.to_string(date), total_balance_neto, total_amount_currency_neto, account))
					datos.append((fields.Date.to_string(date + datetime.timedelta(days=1)), total_balance_detra, total_amount_currency_detra, cuenta_det))
					return datos
				else:
					return [(fields.Date.to_string(date), total_balance, total_amount_currency, account)]

		def _compute_diff_payment_terms_lines(self, existing_terms_lines, account, to_compute):
			''' Process the result of the '_compute_payment_terms' method and creates/updates corresponding invoice lines.
			:param self:                    The current account.move record.
			:param existing_terms_lines:    The current payment terms lines.
			:param account:                 The account.account record returned by '_get_payment_terms_account'.
			:param to_compute:              The list returned by '_compute_payment_terms'.
			'''
			# As we try to update existing lines, sort them by due date.
			existing_terms_lines = existing_terms_lines.sorted(lambda line: line.date_maturity or today)
			existing_terms_lines_index = 0

			# Recompute amls: update existing line or create new one for each payment term.
			new_terms_lines = self.env['account.move.line']
			for date_maturity, balance, amount_currency, cuenta in to_compute:
				currency = self.journal_id.company_id.currency_id
				if currency and currency.is_zero(balance) and len(to_compute) > 1:
					continue

				if existing_terms_lines_index < len(existing_terms_lines):
					# Update existing line.
					candidate = existing_terms_lines[existing_terms_lines_index]
					existing_terms_lines_index += 1
					candidate.update({
						'date_maturity': date_maturity,
						'amount_currency': -amount_currency,
						'debit': balance < 0.0 and -balance or 0.0,
						'credit': balance > 0.0 and balance or 0.0,
					})
				else:
					# Create new line.
					create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
					candidate = create_method({
						'name': self.payment_reference or '',
						'debit': balance < 0.0 and -balance or 0.0,
						'credit': balance > 0.0 and balance or 0.0,
						'quantity': 1.0,
						'amount_currency': -amount_currency,
						'date_maturity': date_maturity,
						'move_id': self.id,
						'currency_id': self.currency_id.id,
						'account_id': cuenta.id,
						'partner_id': self.commercial_partner_id.id,
						'exclude_from_invoice_tab': True,
					})
				new_terms_lines += candidate
				if in_draft_mode:
					candidate.update(candidate._get_fields_onchange_balance(force_computation=True))
			return new_terms_lines

		existing_terms_lines = self.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
		others_lines = self.line_ids.filtered(lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
		company_currency_id = (self.company_id or self.env.company).currency_id
		total_balance = sum(others_lines.mapped(lambda l: company_currency_id.round(l.balance)))
		total_amount_currency = sum(others_lines.mapped('amount_currency'))

		if not others_lines:
			self.line_ids -= existing_terms_lines
			return

		computation_date = _get_payment_terms_computation_date(self)
		account = _get_payment_terms_account(self, existing_terms_lines)
		to_compute = _compute_payment_terms(self, computation_date, total_balance, total_amount_currency, account)
		new_terms_lines = _compute_diff_payment_terms_lines(self, existing_terms_lines, account, to_compute)

		# Remove old terms lines that are no longer needed.
		self.line_ids -= existing_terms_lines - new_terms_lines

		if new_terms_lines:
			self.payment_reference = new_terms_lines[-1].name or ''
			self.invoice_date_due = new_terms_lines[-1].date_maturity



