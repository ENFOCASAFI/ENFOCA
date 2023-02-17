# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DocumentoPago(models.Model):
    _inherit = 'l10n_latam.document.type'
   
    
    #documento_compra_ids = fields.Many2many('l10n_latam.document.type', 'ple_14_report_l10n_latam_id', 'report_14_id', 'doc_14_id', string='Documentos a incluir', required=False, domain="[('type', 'in', [sub_type])]")

    latam_journal_ids = fields.Many2many('account.journal', 'latam_id_account_journal', 'latam_document_id', 'account_journal_id', string='Diarios a incluir', required=False, domain="[('type', 'in', [sub_type])]")


    


