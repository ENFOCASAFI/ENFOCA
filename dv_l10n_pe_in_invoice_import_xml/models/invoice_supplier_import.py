from odoo import api, fields, models
import base64
from xml.dom import minidom


class InvoiceSupplierImport(models.Model):
    _name = 'invoice.supplier.import'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = 'Importar XML de Proveedores'

    name = fields.Char(string='Nombre')
    company_id = fields.Many2one('res.company', string='Compañía', required=True,
                                 readonly=False, default=lambda self: self.env.company)
    journal_id = fields.Many2one('account.journal', string="Diario por defecto", domain=[
        ("type", "=", "purchase")], required=True)
    account_id = fields.Many2one(
        "account.account", string="Cuenta contable por defecto", required=True)
    product_id = fields.Many2one(
        "product.product", string="Producto por defecto", required=True)
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[(
        'res_model', '=', 'invoice.supplier.import')], string='Archivos')
    account_move_ids = fields.One2many(
        "account.move", "invoice_supplier_import_id", string="Facturas de proveedores")
    invoice_count = fields.Integer(
        string='Cantidad de facturas', compute='_compute_invoice_count', readonly=True)

    @api.depends('account_move_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.account_move_ids)

    def action_view_invoice(self):
        """
            Abre el tree de las facturas
        """
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_move_in_invoice_type")
        action['domain'] = [('id', 'in', self.account_move_ids.ids)]
        action['context'] = {
            'default_move_type': 'in_invoice',
        }
        return action

    def action_import_attachments(self):
        for attachment in self.attachment_ids:
            if attachment.mimetype != 'text/xml':
                continue
            decoded_data = base64.b64decode(attachment.datas)
            dom = minidom.parseString(decoded_data)
            # TODO cambiar el nombre del metodo
            #self.obtener_compra_json_de_xml(dom, attachment.datas, attachment.name)
            # TODO mejorar la logica para que itere entre los attachments como en la funcion de arriba
            self.import_invoice_from_xml(
                dom, attachment.datas, attachment.name)

    # Check if the model registry already exists and create it if not
    def create_model_registry_if_not_exists(self, model, model_field, model_field_value, model_registry_data):
        model_registry = self.env[model].search(
            [(model_field, '=', model_field_value)])
        if not model_registry:
            model_registry = self.env[model].create(model_registry_data)
        return model_registry

    def import_invoice_from_xml(self, xml_data, archivo_binario, nombre_binario):
        data_serie = xml_data.getElementsByTagName(
            "cac:Signature")[0].getElementsByTagName("cbc:ID")[0]

        # Create provider
        provider_node = xml_data.getElementsByTagName("cac:SignatoryParty")[0]
        ruc_provider = provider_node.getElementsByTagName("cbc:ID")[
            0].firstChild.data
        provider_data = {
            'name': ruc_provider,
            'company_type': 'company',
            'l10n_latam_identification_type_id': 4,  # RUC
            'vat': ruc_provider
        }
        provider = self.create_model_registry_if_not_exists(
            'res.partner', 'vat', ruc_provider, provider_data)

        # Create account move line (Detalle de factura)
        account_move_lines = []
        details = xml_data.getElementsByTagName("cac:InvoiceLine")
        for detail in details:
            # Producto
            data_producto = detail.getElementsByTagName("cac:Item")[0]
            product_name = data_producto.getElementsByTagName("cbc:Description")[
                0].firstChild.data
            # Cantidad
            data_quantity_node = detail.getElementsByTagName(
                "cbc:InvoicedQuantity")[0]
            quantity = data_quantity_node.firstChild.data
            # Precio unitario
            unit_price = detail.getElementsByTagName(
                "cac:Price")[0].getElementsByTagName("cbc:PriceAmount")[0].firstChild.data
            # Impuestos TODO
            data_taxes_node = detail.getElementsByTagName("cac:TaxTotal")[0]
            detail_data = (0, 0, {
                "product_id": self.product_id.id,
                'product_uom_id': self.product_id.uom_id.id,
                "name": product_name,
                "quantity": quantity,
                "price_unit": unit_price,
                # TODO self.env['account.tax'].search([('name', '=', <TaxScheme> <name>)])
                # 'tax_ids': [(6, 0, self.tax_ids.ids)],
                'account_id': self.account_id.id,
            })
            account_move_lines.append(detail_data)

        # Create account move (Factura de compra)
        invoice_date = xml_data.getElementsByTagName("cbc:IssueDate")[
            0].firstChild.data
        currency = xml_data.getElementsByTagName(
            "cbc:DocumentCurrencyCode")[0].firstChild.data
        currency_odoo = self.env["res.currency"].search(
            [("name", "=", currency)], limit=1)
        document_type = self.env["l10n_latam.document.type"].search(
            [("name", "=", "Factura")], limit=1)
        data_serie = xml_data.getElementsByTagName(
            "cac:Signature")[0].getElementsByTagName("cbc:ID")[0]
        serie_correlativo = data_serie.firstChild.data

        account_move_data = {
            'invoice_user_id': self.env.user.id,
            'partner_id': provider.id,
            'company_id': self.company_id.id,
            'invoice_date': invoice_date,
            'move_type': 'in_invoice',
            "invoice_supplier_import_id": self.id,
            'currency_id': currency_odoo.id,
            'l10n_latam_document_type_id': document_type.id,  # Ruc,
            'ref': serie_correlativo,
            'data_xml': archivo_binario,
            'datas_fname': nombre_binario,
            # "data_pdf": pdf_binary,
            # "datas_fname_pdf": nombre_pdf,
            'invoice_line_ids': account_move_lines
        }

        invoice_id = self.env['account.move'].create(account_move_data)
        invoice_id._onchange_invoice_line_ids()
        for line in invoice_id.invoice_line_ids:
            line._onchange_account_id()
            line._onchange_price_subtotal()
        return "aaa"
