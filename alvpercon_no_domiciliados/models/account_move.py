# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DocumentoPago(models.Model):
	_name = 'tablasunat.nodocumentado'
	_description ="Tabla 32 de Sunat para no Domiciliados"
    
	name = fields.Char(string='Mod. Servicio no Domiciliado')
	codigo = fields.Char(string='Código')

class AccountMove(models.Model):
	_inherit = 'account.move'

	doc_relac_nodomic = fields.Boolean('Selección de documento relacionado')
	nro_doc_id = fields.Many2one("account.move", string='Relación de documentos' , domain="[('pe_invoice_code', 'in', ['46','50','51']),('doc_relac_nodomic', '=', False)]")
	#tipotrab_doc_nodoc = fields.Selection([('1','Intereses provenientes de credito de fomento'),('2','Renta de los inmuebres de propiedad'),('3','Remuneraciones que persiban por ejercicio de su cargo en el pais')],'Documento no domiciliado')
	tipotrab_doc_nodoc_id = fields.Many2one("tablasunat.nodocumentado", string='Mod. Servicio no Domciliado')
	anio_dua = fields.Char('Año de la dua')

	@api.onchange('nro_doc_id')
	def _onchange_nro_doc_id(self):
		for reg in self:
			doc_id = [
					('name','=',reg.nro_doc_id.name)				
			]
			move_doc_id = self.env['account.move'].sudo().search(doc_id)

			if move_doc_id:
				move_doc_id.doc_relac_nodomic = True


