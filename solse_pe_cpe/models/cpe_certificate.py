# -*- coding: utf-8 -*-
# Copyright (c) 2019-2022 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php

from odoo import models, fields, api


class PeCertificate(models.Model):
	_name = 'cpe.certificate'
	_description = 'Certificado Sunat'

	company_id = fields.Many2one(comodel_name='res.company', string='Compañía', required=True, default=lambda self:self.env.user.company_id)
	name = fields.Char("Nombre", required=True)
	start_date = fields.Date("Fecha de inicio", required=True)
	end_date = fields.Date("Fecha fin", required=True)
	state = fields.Selection([
		('draft', 'Borrador'),
		('done', 'Listo'),
		('cancel', 'Cancelado'),
	], string='Status', index=True, readonly=True, default='draft',
		track_visibility='always', copy=False)
	key = fields.Text(".key", required=True)
	crt = fields.Text(".crt", required=True)

	def action_draft(self):
		self.state = "draft"

	def action_done(self):
		self.state = "done"

	def action_cancel(self):
		self.state = "cancel"
