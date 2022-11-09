# -*- coding: utf-8 -*-
# Copyright (c) 2019-2020 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from odoo import models, fields, api
import unicodedata

class City(models.Model):
	_description = "Provincia"
	_inherit = 'res.city'
	
	name_simple = fields.Char('Nombre simple', compute='_compute_nombre_simple', store=True)

	@api.depends('name')
	def _compute_nombre_simple(self):
		for reg in self:
			reg.name_simple = unicodedata.normalize('NFKD', reg.name).encode('ASCII', 'ignore').strip().upper().decode()