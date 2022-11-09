# -*- coding: utf-8 -*-
# Copyright (c) 2019-2020 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from odoo import models, fields, _
from odoo.exceptions import UserError


class ValidateAccountMove(models.TransientModel):
	_name = "solse.busqueda.vat"
	_description = "Validate Account Move"

	force_post = fields.Boolean(string="Force", help="Entries in the future are set to be auto-posted by default. Check this checkbox to post them now.")

	def actualizar_datos_vat(self):
		entidades = self.env['res.partner'].browse(self._context.get('active_ids', []))
		if not entidades:
			raise UserError('No se encuentran ni una seleccion')
		for reg in entidades:
			reg.update_document()
		return {'type': 'ir.actions.act_window_close'}
