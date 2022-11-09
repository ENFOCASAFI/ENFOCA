from odoo import models, fields, api, _
from odoo.tools import float_is_zero

from itertools import chain

class MulticurrencyRevaluationReport(models.Model):
    _inherit = 'account.accounting.report'
    _name = 'account.multicurrency.revaluation.conversion'
    _description = 'Multicurrency Revaluation Report'
    _auto = False

    _order = "report_include desc, currency_code desc, account_code asc, date desc, id desc"

    filter_analytic = True
    filter_multi_company = None
    filter_date = {'filter': 'this_month', 'mode': 'single'}
    filter_all_entries = False
    total_line = False

    report_amount_currency = fields.Monetary(string='Balance in national currency')
    report_amount_currency_current = fields.Monetary(string='Balance at current rate')
    report_adjustment = fields.Monetary(string='Adjustment')
    report_balance = fields.Monetary(string='Balance at operation rate')
    report_currency_id = fields.Many2one('res.currency')
    report_include = fields.Boolean(group_operator='bool_and')
    account_code = fields.Char(group_operator="max")
    account_name = fields.Char(group_operator="max")
    currency_code = fields.Char(group_operator="max")
    move_ref = fields.Char(group_operator="max")
    move_name = fields.Char(group_operator="max")

    @api.model
    def _get_report_name(self):
        return _('Unrealized Conversion Rate')

    @api.model
    def _get_templates(self):
        templates = super()._get_templates()
        templates['line_template'] = 'dv_account_reports_base.line_template_multicurrency_report'
        templates['main_template'] = 'dv_account_reports_base.template_multicurrency_report'
        return templates

    def _get_reports_buttons(self, options):
        r = super()._get_reports_buttons(options)
        r.append({'name': _('Adjustment Entry'), 'action': 'view_revaluation_wizard'})
        return r

    def _get_options(self, previous_options=None):
        options = super()._get_options(previous_options)
        rates = self.env['res.currency'].search([('active', '=', True)], order='rate_type')._get_rates(self.env.company, options.get('date').get('date_to'))
        for key in rates.keys():  # normalize the rates to the company's currency
            rates[key] /= rates[self.env.company.currency_id.id]
        options['currency_rates'] = {
            str(currency_id.id): {
                'currency_id': currency_id.id,
                'rate_type': currency_id.rate_type,
                'display_name': f"{currency_id.name}/Compra" if currency_id.rate_type == 'purchase' else f"{currency_id.name}/Venta",
                'currency_name': f"{currency_id.name}/Compra" if currency_id.rate_type == 'purchase' else f"{currency_id.name}/Venta",
                'currency_main': self.env.company.currency_id.name,
                #'rate': round(1 / rates[currency_id.id], 3),
                'rate': (round(1 / rates[currency_id.id], 3)
                         if not (previous_options or {}).get('currency_rates', {}).get(str(currency_id.id), {}).get('rate') else
                         float(previous_options['currency_rates'][str(currency_id.id)]['rate'])),
            } for currency_id in self.env['res.currency'].search([('active', '=', True)], order='rate_type')
        }
        options['company_currency'] = options['currency_rates'][str(self.env.company.currency_id.id)]
        not_usd_currencies = self.env['res.currency'].search([('active', '=', True), ('name', '!=', 'USD')], order='rate_type')
        for cur in not_usd_currencies:
            options['currency_rates'].pop(str(cur.id))
        options['warning_multicompany'] = len(self.env.companies) > 1
        rates = self.env['res.currency'].search([('active', '=', True)], order='rate_type')._get_rates(self.env.company, options.get('date').get('date_to'))
        for key in rates.keys():  # normalize the rates to the company's currency
            rates[key] /= rates[self.env.company.currency_id.id]
        options['warning_multicompany'] = len(self.env.companies) > 1
        return options

    def _get_column_details(self, options):
        columns_header = [
            self._header_column(),
            self._field_column('report_amount_currency'),
            self._field_column('report_balance'),
            self._field_column('report_amount_currency_current'),
            self._field_column('report_adjustment'),
        ]
        return columns_header

    def _get_hierarchy_details(self, options):
        return [
            self._hierarchy_level('report_include'),
            self._hierarchy_level('report_currency_id'),
            self._hierarchy_level('account_id', foldable=True),
            self._hierarchy_level('id'),
        ]

    # GET LINES VALUES
    def _get_sql(self):
        options = self.env.context['report_options']
        query = '(VALUES {}) AS custom_currency_table(currency_id, currency_name, rate_type, rate)'.format(
            ', '.join("(%s, %s, %s, %s)" for i in range(
                len(options['currency_rates'])))
        )
        params = list(chain.from_iterable(
            (cur['currency_id'], cur['currency_name'], cur['rate_type'], cur['rate']) for cur in options['currency_rates'].values()))
        custom_currency_table = self.env.cr.mogrify(
            query, params).decode(self.env.cr.connection.encoding)
        #WHERE (account.currency_id IS NULL OR aml.currency_id = aml.company_currency_id) AND account.currency_multirate_conversion_affected = TRUE
        # aml.amount_currency / currency_rate.rate - aml.balance AS report_adjustment,
        # aml.balance                                          AS report_balance,
        # (CASE WHEN move.invoice_date IS NOT NULL THEN move.invoice_date ELSE aml.date END)
        # CASE WHEN aml.id = part.credit_move_id THEN part.debit_currency_id ELSE part.credit_currency_id
        #           END                                                  AS report_currency_id,
        return """
            SELECT {move_line_fields},
                   aml.balance                                          AS report_amount_currency,
                   CASE WHEN aml.currency_id = aml.company_currency_id THEN balance * currency_rate.rate ELSE aml.amount_currency END AS report_balance,
                   aml.balance / custom_currency_table.rate             AS report_amount_currency_current,
                   aml.balance / custom_currency_table.rate - CASE WHEN aml.currency_id = aml.company_currency_id THEN balance * currency_rate.rate ELSE aml.amount_currency END AS report_adjustment,
                   account.multirate_conversion_currency_id             AS report_currency_id,
                   account.code                                         AS account_code,
                   account.name                                         AS account_name,
                   currency_rate.currency_display_name                  AS currency_code,
                   move.ref                                             AS move_ref,
                   move.name                                            AS move_name,
                   NOT EXISTS (
                       SELECT * FROM account_account_exclude_res_currency_provision WHERE account_account_id = account_id AND res_currency_id = aml.currency_id
                   )                                                    AS report_include
            FROM account_move_line aml
            JOIN account_move move ON move.id = aml.move_id
            JOIN account_account account ON aml.account_id = account.id
            JOIN res_currency currency ON currency.id = aml.currency_id
            JOIN {custom_currency_table} ON custom_currency_table.currency_id = account.multirate_conversion_currency_id
            JOIN res_currency_rate currency_rate ON currency_rate.currency_name = 'USD' AND currency_rate.currency_rate_type = 'sale' AND currency_rate.name = (CASE WHEN move.invoice_date IS NOT NULL THEN move.invoice_date ELSE aml.date END)
            WHERE (account.currency_id = aml.company_currency_id OR account.currency_id IS NULL) AND account.currency_multirate_conversion_affected = TRUE
            {account_query}
        """.format(
            custom_currency_table=custom_currency_table,
            move_line_fields=self._get_move_line_fields('aml'),
            account_query=self._get_account_query(options),
        )

    def _format_all_line(self, res, value_dict, options):
        if value_dict.get('report_currency_id'):
            report_currency_code = self.env['res.currency'].browse(value_dict.get('report_currency_id')[0])
            res['columns'][1] = {'name': self.format_value(value_dict['report_balance'], report_currency_code)}
            res['columns'][2] = {'name': self.format_value(value_dict['report_amount_currency_current'], report_currency_code)}
            res['columns'][3] = {'name': self.format_value(value_dict['report_adjustment'], report_currency_code)}
        res['included'] = value_dict.get('report_included')
        res['class'] = 'no_print' if not value_dict.get('report_include') else ''

    def _format_report_currency_id_line(self, res, value_dict, options):
        res['name'] = '{for_cur} (1 {comp_cur} = {rate:.6} {for_cur})'.format(
            for_cur=value_dict['currency_code'],
            comp_cur=self.env.company.currency_id.name,
            rate=float(options['currency_rates'][str(value_dict.get('report_currency_id')[0])]['rate']),
        )

    def _format_account_id_line(self, res, value_dict, options):
        res['name'] = '%s %s' % (value_dict['account_code'], value_dict['account_name'])

    def _format_id_line(self, res, value_dict, options):
        res['name'] = self._format_aml_name(value_dict['name'], value_dict['move_ref'], value_dict['move_name'])
        res['caret_options'] = 'account.move'

    def _format_report_include_line(self, res, value_dict, options):
        res['name'] = _('Accounts to adjust') if value_dict.get('report_include') else _('Excluded Accounts')
        res['columns'] = [{}, {}, {}, {}]

    # ACTIONS
    def toggle_provision(self, options, params):
        """Include/exclude an account from the provision."""
        account = self.env['account.account'].browse(int(params.get('account_id')))
        currency = self.env['res.currency'].browse(int(params.get('currency_id')))
        if currency in account.exclude_provision_currency_ids:
            account.exclude_provision_currency_ids -= currency
        else:
            account.exclude_provision_currency_ids += currency
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def view_revaluation_wizard(self, context):
        """Open the revaluation wizard."""
        form = self.env.ref('dv_account_multicurrency_revaluation_multirate_conversion.view_account_multicurrency_revaluation_conversion_wizard', False)
        return {
            'name': _('Make Adjustment Entry'),
            'type': 'ir.actions.act_window',
            'res_model': "account.multicurrency.revaluation.conversion.wizard",
            'view_mode': "form",
            'view_id': form.id,
            'views': [(form.id, 'form')],
            'multi': "True",
            'target': "new",
            'context': context,
        }

    def view_currency(self, options, params=None):
        """Open the currency rate list."""
        id = params.get('id')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Currency Rates (%s)', self.env['res.currency'].browse(id).display_name),
            'views': [(False, 'list')],
            'res_model': 'res.currency.rate',
            'context': {**self.env.context, **{'default_currency_id': id}},
            'domain': [('currency_id', '=', id)],
        }

    def _get_account_query(self, options):
        account_query = ''
        if options.get('accounts'):
            account_list = options.get('accounts')
            if len(account_list) == 1:
                account = account_list[0]
                account_query = """ AND aml.account_id = %s""" % (
                    str(account))
            else:
                accounts = tuple(list(set(account_list)))
                account_query = """ AND aml.account_id in %s""" % (
                    str(tuple(accounts)))
        return account_query
