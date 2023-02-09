# -*- coding: utf-8 -*-
# Copyright (c) 2019-2020 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class GenerarAsientosDestino(models.TransientModel):
	_name = 'saccount.generar.asientos.destino'
	_description = 'Generar Asiento Destino'

	fecha_ini = fields.Date("Fecha inicial")
	fecha_fin = fields.Date("Fecha fin")

	
	def crear_movimientos(self):
		#self.env['account.move'].generar_asientos_destino_falantes()
		dominio = [("move_type", "in", ["in_invoice", "entry"]), ("state", "=", "posted"), ("target_move_count", "=", 0)]
		if self.fecha_ini and self.fecha_fin:
			dominio.extend([('date', '>=', self.fecha_ini), ('date', '<=', self.fecha_fin)])
		facturas = self.env['account.move'].search(dominio)
		for move in facturas:
			try:
				move.crear_asiento_destino()
			except Exception as e:
				raise UserError("%s (%s)" % (str(e), move.name))
		
		return {
			'type': 'ir.actions.client',
			'tag': 'display_notification',
			'params': {
				'type': 'info',
				'title': _('Proceso terminado exitosamente'),
				'sticky': False,
				'next': {'type': 'ir.actions.act_window_close'},
			}
		}
