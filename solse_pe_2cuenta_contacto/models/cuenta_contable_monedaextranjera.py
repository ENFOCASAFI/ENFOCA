# -*- coding: utf-8 -*-
# Copyright (c) 2019-2022 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php

from odoo import api, fields, models, _
import logging
from odoo.exceptions import UserError, RedirectWarning
import json
_logging = logging.getLogger(__name__)

class AccountMove(models.Model):
	_inherit = 'account.move'

	def obtener_cuenta_mextranejera_cliente(self, contacto):
		if self.move_type == 'out_invoice':
			if self.currency_id.id != self.company_id.currency_id.id:
				return self.partner_id.property_account_receivable_2_id or self.partner_id.property_account_receivable_id
		
		return self.partner_id.property_account_receivable_id

	def obtener_cuenta_mextranejera_proveedor(self, contacto):
		_logging.info("Cuenta de proveedor")
		if self.move_type == 'in_invoice':
			if self.currency_id.id != self.company_id.currency_id.id:
				return self.partner_id.property_account_payable_2_id or self.partner_id.property_account_payable_id
		
		return self.partner_id.property_account_payable_id

	@api.onchange('currency_id', 'line_ids')
	def _onchange_adicional_id(self):
		if not self.partner_id:
			return

		warning = {}
		if self.partner_id:
			rec_account = self.obtener_cuenta_mextranejera_cliente(self.partner_id)
			pay_account = self.obtener_cuenta_mextranejera_proveedor(self.partner_id)
			if not rec_account and not pay_account:
				action = self.env.ref('account.action_account_config')
				msg = _('Cannot find a chart of accounts for this company, You should configure it. \nPlease go to Account Configuration.')
				msg = msg + " "+self.partner_id.name
				raise RedirectWarning(msg, action.id, _('Go to the configuration panel'))
			p = self.partner_id
			if p.invoice_warn == 'no-message' and p.parent_id:
				p = p.parent_id
			if p.invoice_warn and p.invoice_warn != 'no-message':
				# Block if partner only has warning but parent company is blocked
				if p.invoice_warn != 'block' and p.parent_id and p.parent_id.invoice_warn == 'block':
					p = p.parent_id
				warning = {
					'title': _("Warning for %s", p.name),
					'message': p.invoice_warn_msg
				}
				if p.invoice_warn == 'block':
					self.partner_id = False
					return {'warning': warning}

		if self.is_sale_document(include_receipts=True) and self.partner_id:
			self.invoice_payment_term_id = self.partner_id.property_payment_term_id or self.invoice_payment_term_id
			new_term_account = self.obtener_cuenta_mextranejera_cliente(self.partner_id.commercial_partner_id)
		elif self.is_purchase_document(include_receipts=True) and self.partner_id:
			self.invoice_payment_term_id = self.partner_id.property_supplier_payment_term_id or self.invoice_payment_term_id
			new_term_account = self.obtener_cuenta_mextranejera_proveedor(self.partner_id.commercial_partner_id)
		else:
			new_term_account = None

		for line in self.line_ids:
			line.partner_id = self.partner_id.commercial_partner_id

			if new_term_account and line.account_id.user_type_id.type in ('receivable', 'payable'):
				line.account_id = new_term_account

		self._compute_bank_partner_id()
		bank_ids = self.bank_partner_id.bank_ids.filtered(lambda bank: bank.company_id is False or bank.company_id == self.company_id)
		self.partner_bank_id = bank_ids and bank_ids[0]

		# Find the new fiscal position.
		delivery_partner_id = self._get_invoice_delivery_partner_id()
		self.fiscal_position_id = self.env['account.fiscal.position'].get_fiscal_position(
			self.partner_id.id, delivery_id=delivery_partner_id)
		self._recompute_dynamic_lines()
		if warning:
			return {'warning': warning}

	@api.onchange('partner_id')
	def _onchange_partner_id(self):
		self = self.with_company(self.journal_id.company_id)

		warning = {}
		if self.partner_id:
			rec_account = self.obtener_cuenta_mextranejera_cliente(self.partner_id)
			pay_account = self.obtener_cuenta_mextranejera_proveedor(self.partner_id)
			if not rec_account and not pay_account:
				action = self.env.ref('account.action_account_config')
				msg = _('Cannot find a chart of accounts for this company, You should configure it. \nPlease go to Account Configuration.')
				msg = msg + " "+self.partner_id.name
				raise RedirectWarning(msg, action.id, _('Go to the configuration panel'))
			p = self.partner_id
			if p.invoice_warn == 'no-message' and p.parent_id:
				p = p.parent_id
			if p.invoice_warn and p.invoice_warn != 'no-message':
				# Block if partner only has warning but parent company is blocked
				if p.invoice_warn != 'block' and p.parent_id and p.parent_id.invoice_warn == 'block':
					p = p.parent_id
				warning = {
					'title': _("Warning for %s", p.name),
					'message': p.invoice_warn_msg
				}
				if p.invoice_warn == 'block':
					self.partner_id = False
					return {'warning': warning}

		if self.is_sale_document(include_receipts=True) and self.partner_id:
			self.invoice_payment_term_id = self.partner_id.property_payment_term_id or self.invoice_payment_term_id
			new_term_account = self.obtener_cuenta_mextranejera_cliente(self.partner_id.commercial_partner_id)
		elif self.is_purchase_document(include_receipts=True) and self.partner_id:
			self.invoice_payment_term_id = self.partner_id.property_supplier_payment_term_id or self.invoice_payment_term_id
			new_term_account = self.obtener_cuenta_mextranejera_proveedor(self.partner_id.commercial_partner_id)
		else:
			new_term_account = None

		for line in self.line_ids:
			line.partner_id = self.partner_id.commercial_partner_id

			if new_term_account and line.account_id.user_type_id.type in ('receivable', 'payable'):
				line.account_id = new_term_account

		self._compute_bank_partner_id()
		bank_ids = self.bank_partner_id.bank_ids.filtered(lambda bank: bank.company_id is False or bank.company_id == self.company_id)
		self.partner_bank_id = bank_ids and bank_ids[0]

		# Find the new fiscal position.
		delivery_partner_id = self._get_invoice_delivery_partner_id()
		self.fiscal_position_id = self.env['account.fiscal.position'].get_fiscal_position(
			self.partner_id.id, delivery_id=delivery_partner_id)
		self._recompute_dynamic_lines()
		if warning:
			return {'warning': warning}


	"""def _recompute_payment_terms_lines(self):
		self.ensure_one()
		self = self.with_company(self.company_id)
		in_draft_mode = self != self._origin
		today = fields.Date.context_today(self)
		self = self.with_company(self.journal_id.company_id)

		def _get_payment_terms_computation_date(self):
			if self.invoice_payment_term_id:
				return self.invoice_date or today
			else:
				return self.invoice_date_due or self.invoice_date or today

		def _get_payment_terms_account(self, payment_terms_lines):
			if payment_terms_lines:
				# Retrieve account from previous payment terms lines in order to allow the user to set a custom one.
				return payment_terms_lines[0].account_id
			elif self.partner_id:
				# Retrieve account from partner.
				if self.is_sale_document(include_receipts=True):
					return self.obtener_cuenta_mextranejera_cliente(self.partner_id)
				else:
					return self.obtener_cuenta_mextranejera_proveedor(self.partner_id)
			else:
				# Search new account.
				domain = [
					('company_id', '=', self.company_id.id),
					('internal_type', '=', 'receivable' if self.move_type in ('out_invoice', 'out_refund', 'out_receipt') else 'payable'),
				]
				return self.env['account.account'].search(domain, limit=1)

		def _compute_payment_terms(self, date, total_balance, total_amount_currency):
			if self.invoice_payment_term_id:
				to_compute = self.invoice_payment_term_id.compute(total_balance, date_ref=date, currency=self.company_id.currency_id)
				if self.currency_id == self.company_id.currency_id:
					# Single-currency.
					return [(b[0], b[1], b[1]) for b in to_compute]
				else:
					# Multi-currencies.
					to_compute_currency = self.invoice_payment_term_id.compute(total_amount_currency, date_ref=date, currency=self.currency_id)
					return [(b[0], b[1], ac[1]) for b, ac in zip(to_compute, to_compute_currency)]
			else:
				return [(fields.Date.to_string(date), total_balance, total_amount_currency)]

		def _compute_diff_payment_terms_lines(self, existing_terms_lines, account, to_compute):
			existing_terms_lines = existing_terms_lines.sorted(lambda line: line.date_maturity or today)
			existing_terms_lines_index = 0

			# Recompute amls: update existing line or create new one for each payment term.
			new_terms_lines = self.env['account.move.line']
			for date_maturity, balance, amount_currency in to_compute:
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
						'account_id': account.id,
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
		to_compute = _compute_payment_terms(self, computation_date, total_balance, total_amount_currency)
		new_terms_lines = _compute_diff_payment_terms_lines(self, existing_terms_lines, account, to_compute)

		# Remove old terms lines that are no longer needed.
		self.line_ids -= existing_terms_lines - new_terms_lines

		if new_terms_lines:
			self.payment_reference = new_terms_lines[-1].name or ''
			self.invoice_date_due = new_terms_lines[-1].date_maturity"""