# -*- coding: utf-8 -*-
# Copyright (c) 2019-2022 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning

class CompanyConf(models.Model):
	_name = 'res.company.conf'
	_description = 'Configuración de empresa'

	name = fields.Char('Nombre', default='Configuración empresa')
	company_id = fields.Many2one('res.company', 'Empresa')
	sunat_amount = fields.Float(string="Monto", help="Usado para el control de boletas", digits=(16, 2), default=700)
	cuenta_detraccion = fields.Many2one('account.journal', string='Cuenta de Detracción', domain="[('type','=', 'bank')]")
	monto_detraccion = fields.Float(string='Monto detracción', help="Monto usado para determinar cuando aplicar detracción", default=750)
	agente_retencion = fields.Boolean('Es agente de retención')
	por_retencion = fields.Float('% Retención', default=3.0)