from odoo import models, fields


class import_xml(models.Model):
    _inherit = 'account.move'

    invoice_supplier_import_id = fields.Many2one(
        'invoice.supplier.import', string='Importar XML')
    datas_fname = fields.Char("Nombre xml")
    data_xml = fields.Binary(string="XML")
    datas_fname_pdf = fields.Char("Nombre pdf")
    data_pdf = fields.Binary(string="PDF")
