# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
import logging
_logging = logging.getLogger(__name__)

class AccountMove(models.Model) :
	_inherit = 'account.move'

	pago_detraccion = fields.Many2one('account.payment', 'Pago de Detracción/Retención')