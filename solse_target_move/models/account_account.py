# -*- coding: utf-8 -*-
# Copyright (c) 2019-2020 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.


import time
import math
import re

from odoo.osv import expression
from odoo.tools.float_utils import float_round as round, float_compare
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _, tools
from odoo.tests.common import Form


class AccountAccount(models.Model):
	_inherit = "account.account"
	
	debit_target_account_id = fields.Many2one('account.account', string='Cuenta destino de débito')
	credit_target_account_id = fields.Many2one('account.account', string='Cuenta destino de crédito')
	target_journal_id = fields.Many2one('account.journal', string='Diario de destino')
	target_account = fields.Boolean(string='Tiene cuenta de destino', default=False)
	
