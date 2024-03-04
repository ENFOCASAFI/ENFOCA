from odoo import api, fields, models, _
from odoo.exceptions import UserError

class BalanceDate(models.TransientModel):    
    _name = "balance.date.report"
    _description = "Fecha Reporte de Balance"

    fecha_ini=fields.Date("Fecha Inicial")
    fecha_fin=fields.Date("Fecha Final")
    fecha_fin_acum=fields.Date("Fecha Final Acum.")
    fecha_ini_comp=fields.Date("Fecha Inicial")
    fecha_fin_comp=fields.Date("Fecha Final")
    fecha_fin_comp_acum=fields.Date("Fecha Final Acum.")
    is_mensual = fields.Boolean("Mensual")
    is_mensual = fields.Boolean("Mensual")
    is_acumulado = fields.Boolean("Acumulado")
    is_mensual_comp = fields.Boolean("Mensual Comparaivo")  
    is_acumulado_comp = fields.Boolean("Acumulado Comparativo") 
    
    def print_report(self):
        #print("Vamos bien!!!")

        query ="UPDATE account_move_line SET account_for_balance = 0; "
        self.env.cr.execute(query)

        self.env.cr.execute("""UPDATE account_move_line 
                                SET account_for_balance = 1
                                WHERE date >= %s 
                                AND date <= %s;
        """, [self.fecha_ini, self.fecha_fin])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Reporte Balance',
            'res_model': 'balance.record.group',
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

        self.env.cr.execute("""UPDATE account_move_line 
                                SET account_for_balance = 1
                                WHERE date >= %s 
                                AND date <= %s;
        """, [self.fecha_ini, self.fecha_fin])

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

