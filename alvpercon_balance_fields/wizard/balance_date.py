from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class BalanceDate(models.TransientModel):    
    _name = "balance.date.report"
    _description = "Fecha Reporte de Balance"

    fecha_ini=fields.Date("Fecha Inicial" , default=lambda self: fields.Date.context_today(self).replace(year=2022, month=1, day=1))
    fecha_fin=fields.Date("Fecha Final" , default=fields.Date.context_today)
    fecha_fin_acum=fields.Date("Fecha Final Acum." , default=fields.Date.context_today)
    fecha_ini_comp=fields.Date("Fecha Inicial Comp." , default=lambda self: fields.Date.context_today(self).replace(year=2022, month=1, day=1))
    fecha_fin_comp=fields.Date("Fecha Final Comp." , default=fields.Date.context_today)
    fecha_fin_comp_acum=fields.Date("Fecha Final Comp. Acum." , default=fields.Date.context_today)
    journalb_ids = fields.Many2many('account.journal', 'nf_balance_table','balance_ids' ,'journal_ids' , string='Diarios Contables')
    #is_mensual = fields.Boolean("Mensual")
    is_mensual = fields.Boolean("Periodo")
    is_acumulado = fields.Boolean("Acumulado")
    is_mensual_comp = fields.Boolean("Comparativo")  
    is_acumulado_comp = fields.Boolean("Acumulado Comparativo")
    is_saldo_ini = fields.Boolean("Filtro de Diarios Contables")

      
    
    def print_report(self):
        #print("Vamos bien!!!")
        query ="UPDATE account_move_line SET account_for_balance = 0; "        
        self.env.cr.execute(query)

        query1 ="UPDATE account_move_line SET account_saldo_ini = ''; "        
        self.env.cr.execute(query1)

        list_ids = []
        journalsf_ids = ()
        for list_b in  self.journalb_ids:
            list_ids.append(list_b.id)

        journalsf_ids = tuple(list_ids)      

        if self.is_mensual:

            self.env.cr.execute("""UPDATE account_move_line 
                                    SET account_for_balance = 1
                                    WHERE date >= %s 
                                    AND date <= %s;
            """, [self.fecha_ini, self.fecha_fin])

            # self.env.cr.execute("""UPDATE account_move_line SET account_saldo_ini = account_journal.name
            #                     FROM account_journal WHERE account_move_line.journal_id = account_journal.id
            #                     AND account_journal.name like '%APERT%';
            # """)
            
        
        if self.is_saldo_ini:

            self.env.cr.execute("""UPDATE account_move_line 
                                    SET account_saldo_ini = 'a'
                                    WHERE journal_id in %s;
            """, [journalsf_ids])

            query2 ="UPDATE account_move_line SET account_for_balance = 0 WHERE account_saldo_ini = 'a'; "        
            self.env.cr.execute(query2)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Reporte Balance de Comprobación Soles',
            'res_model': 'balance.record.group',
            'view_type': 'form',
            'view_id': False,
            'view_mode': 'tree,form,pivot',
            'context': {'search_default_grupo_de_cuentas': 1,},
            'target': 'current',
        }

    def print_report_periodo(self):
        # print("Vamos bien!!!")
        query ="UPDATE account_move_line SET account_for_balance_comp = 0; "        
        self.env.cr.execute(query)

        query1 ="UPDATE account_move_line SET account_filtered_comp = ''; "        
        self.env.cr.execute(query1)

        list_ids = []
        journalsf_ids = ()
        for list_b in  self.journalb_ids:
            list_ids.append(list_b.id)

        journalsf_ids = tuple(list_ids)      

        if self.is_mensual_comp:

            self.env.cr.execute("""UPDATE account_move_line 
                                    SET account_for_balance_comp = 1
                                    WHERE date >= %s 
                                    AND date <= %s;
            """, [self.fecha_ini, self.fecha_fin])
            
        
            self.env.cr.execute("""UPDATE account_move_line 
                                    SET account_for_balance_comp = 1
                                    WHERE date >= %s 
                                    AND date <= %s;
            """, [self.fecha_ini_comp, self.fecha_fin_comp])
            
        
        if self.is_saldo_ini:

            self.env.cr.execute("""UPDATE account_move_line 
                                    SET account_filtered_comp = 'a'
                                    WHERE journal_id in %s;
            """, [journalsf_ids])

            query2 ="UPDATE account_move_line SET account_for_balance = 0 WHERE account_filtered_comp = 'a'; "        
            self.env.cr.execute(query2)


        return {
            'type': 'ir.actions.act_window',
            'name': 'Reporte Balance por Periodo',
            'res_model': 'balance.record.group.periodo',
            'view_type': 'form',
            'view_id': False,
            'view_mode': 'tree,form,pivot',
            'context': {'search_default_grupo_de_cuentas': 1,},
            'target': 'current',
        }


    
    def print_report_dolares(self):
        #print("Vamos bien!!!")

        query ="UPDATE account_move_line SET account_for_balance = 0; "        
        self.env.cr.execute(query)

        query1 ="UPDATE account_move_line SET account_saldo_ini = ''; "        
        self.env.cr.execute(query1)

        list_ids = []
        journalsf_ids = ()
        for list_b in  self.journalb_ids:
            list_ids.append(list_b.id)

        journalsf_ids = tuple(list_ids)      

        if self.is_mensual:

            self.env.cr.execute("""UPDATE account_move_line 
                                    SET account_for_balance = 1
                                    WHERE date >= %s 
                                    AND date <= %s;
            """, [self.fecha_ini, self.fecha_fin])

        
        if self.is_saldo_ini:

            self.env.cr.execute("""UPDATE account_move_line 
                                    SET account_saldo_ini = 'a'
                                    WHERE journal_id in %s;
            """, [journalsf_ids])

            query2 ="UPDATE account_move_line SET account_for_balance = 0 WHERE account_saldo_ini = 'a'; "        
            self.env.cr.execute(query2)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Reporte Balance de Comprobación USD',
            'res_model': 'balance.record.group.dolar',
            'view_type': 'form',
            'view_id': False,
            'view_mode': 'tree,form,pivot',
            'context': {'search_default_grupo_de_cuentas': 1,},
            'target': 'current',
        }


        #journal_id not in (107,108,109)

    @api.onchange('fecha_fin_comp_acum')
    def onchange_fecha_fin_comp_acum(self):
            self.fecha_fin_acum = self.fecha_fin_comp_acum + relativedelta(years=-1)

    @api.onchange('fecha_ini_comp')
    def onchange_fecha_ini_comp(self):
            self.fecha_ini = self.fecha_ini_comp + relativedelta(years=-1)
    
    @api.onchange('fecha_fin_comp')
    def onchange_fecha_fin_comp(self):
            self.fecha_fin = self.fecha_fin_comp + relativedelta(years=-1)

    @api.onchange('is_mensual')
    def onchange_is_mensual(self):
        if self.is_mensual :
            self.is_acumulado = False
            self.is_mensual_comp = False
            self.is_acumulado_comp = False
            self.is_saldo_ini = False
            self.fecha_fin = fields.Date.context_today(self)
    
    @api.onchange('is_acumulado')
    def onchange_is_acumulado(self):
        if self.is_acumulado :
            self.is_mensual = False
            self.is_mensual_comp = False
            self.is_acumulado_comp = False
            self.is_saldo_ini = False
    
    @api.onchange('is_mensual_comp')
    def onchange_is_mensual_comp(self):
        if self.is_mensual_comp :
            self.is_mensual = False
            self.is_acumulado = False
            self.is_acumulado_comp = False
            self.is_saldo_ini = False
            self.fecha_fin = self.fecha_fin_comp + relativedelta(years=-1)
    
    @api.onchange('is_acumulado_comp')
    def onchange_is_acumulado_comp(self):
        if self.is_acumulado_comp :
            self.is_mensual = False
            self.is_acumulado = False
            self.is_mensual_comp = False
            self.fecha_fin_acum = self.fecha_fin_comp_acum + relativedelta(years=-1)

        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Reporte Balance',
        #     'res_model': 'balance.record.group.dolar',
        #     'view_type': 'form',
        #     'view_id': False,
        #     'view_mode': 'tree,form',
        #     'target': 'current',
        # }
        
        # data=self.env['account.move.line']

        
        # periodo=[('date','>=',self.fecha_ini),('date','<=',self.fecha_fin)]

        # result = data.search(periodo)

        # for rec in result:
        #     rec.account_for_balance = 1

