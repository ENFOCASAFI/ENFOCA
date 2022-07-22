from odoo import models, fields
import requests
import json
import xmltodict
import base64
from xml.dom import minidom


class import_xml(models.Model):
    _inherit = 'account.move'
    
    invoice_supplier_import_id = fields.Many2one('invoice.supplier.import', string='Importar XML')
    datas_fname = fields.Char("Nombre xml")
    data_xml = fields.Binary(string="XML")
    datas_fname_pdf = fields.Char("Nombre pdf")
    data_pdf = fields.Binary(string="PDF")

    # xml_string to dom.xml
    def xml_string_to_dom_xml(self, xml_string):
        return minidom.parseString(xml_string)

    # Check if the model registry already exists and create it if not
    def create_model_registry_if_not_exists(self, model, model_field, model_field_value, model_registry_data):
        model_registry = self.env[model].search([(model_field, '=', model_field_value)])
        if not model_registry:
            model_registry = self.env[model].create(model_registry_data)
        return model_registry

    # Complete all the fields related to an account move
    def xml_to_json(self):
        obj = ("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
         xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
         xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
         xmlns:ccts="urn:un:unece:uncefact:documentation:2"
         xmlns:cec="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"
         xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
         xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"
         xmlns:qdt="urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2"
         xmlns:sac="urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1"
         xmlns:udt="urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2"
         xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ext:UBLExtensions>
        <ext:UBLExtension>
            <ext:ExtensionContent>
                <ds:Signature Id="F001-43582">
                    <ds:SignedInfo>
                        <ds:CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
                        <ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
                        <ds:Reference URI="">
                            <ds:Transforms>
                                <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
                            </ds:Transforms>
                            <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
                            <ds:DigestValue>Z3Sx+sPuIc0RWNxsuiXicQwv1mo=</ds:DigestValue>
                        </ds:Reference>
                    </ds:SignedInfo>
                    <ds:SignatureValue>B2hy8TSUEFleD1Omr3bNFqJwUrA6k9HmYOKF8uSdvmJoPYDq7Yg8Rrg7Yp9GcgNw65QY05TAqmTO
                        js/iCV6B/Y55sN316ge+y6Gdlex2rc404RfLHzhtukjRyVwQpFhonJWwU+p+bLRPnFSVI8V/jseY
                        KFxFiI8npbIx7idvFEX7WRm4VDMS3OCwGQiK1OQm8L8MHh6fihaaOL0kbFsDLGTiahMwEaZ/Mqni
                        XYS2J2Xyv+Ex8B3r0fKrTRDd0yoGPCiKEi8bq26ogCb8NJJL8pstQiEefT5D+6GTpJKBm65yXgy2
                        4G6ZKgr6oH3I/jXslW3uiWnsdI3k6mHLPqfGAg==
                    </ds:SignatureValue>
                    <ds:KeyInfo>
                        <ds:X509Data>
                            <ds:X509SubjectName>C=PE,O=CAVALI S.A.
                                I.C.L.V.,2.5.4.97=#0c0b3230333436363639363235,OU=Issued by PERUMEDIA [PE1],OU=GERENCIA
                                DE ADMINISTRACION\, FINANZAS Y
                                CONTABILIDAD,2.5.4.12=#0c3653554220474552454e54452044452041444d494e495354524143494f4e2c2046494e414e5a4153205920434f4e544142494c49444144,ST=LIMA
                                - LIMA,L=SAN
                                ISIDRO,2.5.4.5=#130c444e493a3038373533353132,2.5.4.4=#0c124c4f50455a204652414e4349534b4f564943,2.5.4.42=#0c0c564954414c494120524f5341,CN=VITALIA
                                ROSA LOPEZ FRANCISKOVIC,1.2.840.113549.1.9.1=#1611766c6f70657a4062766c2e636f6d2e7065
                            </ds:X509SubjectName>
                            <ds:X509Certificate>
                                MIIJezCCB2OgAwIBAgIJc34qZF0+zIXEMA0GCSqGSIb3DQEBCwUAMIIBIjELMAkGA1UEBhMCUEUx
                                DTALBgNVBAgMBExJTUExDTALBgNVBAcMBExJTUExPTA7BgNVBAsMNHNlZSBjdXJyZW50IGFkZHJl
                                c3MgYXQgd3d3LmNhbWVyZmlybWEuY29tLnBlL2FkZHJlc3MxMDAuBgNVBAsMJ0FDIENBTUVSRklS
                                TUEgUEVSw5ogQ0VSVElGSUNBRE9TIC0gMjAxNjEUMBIGA1UEBRMLMjA1NjYzMDI0NDcxGjAYBgNV
                                BGEMEU5UUlBFLTIwNTY2MzAyNDQ3MSAwHgYDVQQKDBdDQU1FUkZJUk1BIFBFUsOaIFMuQS5DLjEw
                                MC4GA1UEAwwnQUMgQ0FNRVJGSVJNQSBQRVLDmiBDRVJUSUZJQ0FET1MgLSAyMDE2MB4XDTIxMDYx
                                MTIxNDA1N1oXDTIzMDYxMTIxNDA1N1owggGoMSAwHgYJKoZIhvcNAQkBFhF2bG9wZXpAYnZsLmNv
                                bS5wZTEoMCYGA1UEAwwfVklUQUxJQSBST1NBIExPUEVaIEZSQU5DSVNLT1ZJQzEVMBMGA1UEKgwM
                                VklUQUxJQSBST1NBMRswGQYDVQQEDBJMT1BFWiBGUkFOQ0lTS09WSUMxFTATBgNVBAUTDEROSTow
                                ODc1MzUxMjETMBEGA1UEBwwKU0FOIElTSURSTzEUMBIGA1UECAwLTElNQSAtIExJTUExPzA9BgNV
                                BAwMNlNVQiBHRVJFTlRFIERFIEFETUlOSVNUUkFDSU9OLCBGSU5BTlpBUyBZIENPTlRBQklMSURB
                                RDE8MDoGA1UECwwzR0VSRU5DSUEgREUgQURNSU5JU1RSQUNJT04sIEZJTkFOWkFTIFkgQ09OVEFC
                                SUxJREFEMSMwIQYDVQQLDBpJc3N1ZWQgYnkgUEVSVU1FRElBICBbUEUxXTEUMBIGA1UEYQwLMjAz
                                NDY2Njk2MjUxHTAbBgNVBAoMFENBVkFMSSBTLkEuIEkuQy5MLlYuMQswCQYDVQQGEwJQRTCCASIw
                                DQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOF5pPucR6tH6zbD9QDzgsslpeShQj1gGhu3jOZZ
                                D6RAEhXVzU1ajeumkq3pZeFbbRuEAAXYcDcSw/uQfmoqJ6kISeLXmNq7JBNgFoelERFEJwHsOJ0r
                                Ss5wnJiUJdjEUodnHkj79WDTTYvXtM9BpqTrcMzptLGltZdy9pyqXhCn1H4BV8xqDzgQ/yMvS5OR
                                TXER4ezTrvZi2LOESIcp16ik4sKbdyGa5phgcB7TiAf/W1jyZnN53fWdl3IaeaBDAdbhArGdlD4H
                                a/KQW4j4cah+gUwFTbPvgI3S1D00IgEoAo7nk2UcUuCEqd1llVoOPAF96kgv0wCMsdAjtCVu3BkC
                                AwEAAaOCAygwggMkMAwGA1UdEwEB/wQCMAAwDgYDVR0PAQH/BAQDAgbAMB0GA1UdJQQWMBQGCCsG
                                AQUFBwMCBggrBgEFBQcDBDAdBgNVHQ4EFgQUAKjw6es+jsCcBAs+5SpLT84iv00wgY0GCCsGAQUF
                                BwEBBIGAMH4wVAYIKwYBBQUHMAKGSGh0dHA6Ly93d3cuY2FtZXJmaXJtYS5jb20vY2VydHMvYWNf
                                Y2FtZXJmaXJtYV9wZXJ1X2NlcnRpZmljYWRvcy0yMDE2LmNydDAmBggrBgEFBQcwAYYaaHR0cDov
                                L29jc3AuY2FtZXJmaXJtYS5jb20wHwYDVR0jBBgwFoAUOm5lGOdW0uTzLd2lfHJt/zDhhicwgaAG
                                A1UdHwSBmDCBlTBIoEagRIZCaHR0cDovL2NybC5jYW1lcmZpcm1hLmNvbS9hY19jYW1lcmZpcm1h
                                X3BlcnVfY2VydGlmaWNhZG9zLTIwMTYuY3JsMEmgR6BFhkNodHRwOi8vY3JsMS5jYW1lcmZpcm1h
                                LmNvbS9hY19jYW1lcmZpcm1hX3BlcnVfY2VydGlmaWNhZG9zLTIwMTYuY3JsMIHABgNVHREEgbgw
                                gbWBEXZsb3BlekBidmwuY29tLnBlpIGfMIGcMRwwGgYKKwYBBAGBhy4eBwwMVklUQUxJQSBST1NB
                                MRUwEwYKKwYBBAGBhy4eCAwFTE9QRVoxHDAaBgorBgEEAYGHLh4JDAxGUkFOQ0lTS09WSUMxRzBF
                                BgorBgEEAYGHLh4KDDdDRVJUSUZJQ0FETyBERSBQRVJTT05BIEZJU0lDQSBDT04gVklOQ1VMQUNJ
                                T04gQSBFTVBSRVNBMBwGA1UdEgQVMBOBEWNhQGNhbWVyZmlybWEuY29tMIGQBgNVHSAEgYgwgYUw
                                gYIGDCsGAQQBgYcuHhAAATByMCkGCCsGAQUFBwIBFh1odHRwczovL3BvbGljeS5jYW1lcmZpcm1h
                                LmNvbTBFBggrBgEFBQcCAjA5DDdDRVJUSUZJQ0FETyBERSBQRVJTT05BIEZJU0lDQSBDT04gVklO
                                Q1VMQUNJT04gQSBFTVBSRVNBMA0GCSqGSIb3DQEBCwUAA4ICAQBhpHel1rmN9jKmxtwdqVRm42b2
                                w0FVbEJU9FflaTGYRNc2tX6LLyejGvSvUywnl+/hjEagW7/xt+1I1pTa8pKVXOZE699Po1wxT1qd
                                K/yJFE7UC50y/EHMDZ2Xld0bmhKxqHJchXg6SAwo9HLvA5sfQOV/ejSWqf9r6E5uNo+IgwpXg5Zw
                                rORlGqgsvcmG3KmAolJZUJEiYW/1/GjrrjHptCl4C6uqCqAUtOMaQWl51o31Jp22LIZKrvN7yudg
                                gA1BlK6mNa++zKC+i9aVHjOMj4+IH3J7yOazMxcW9Gg4wpRDOFAI/Xxo6h6EL7yYvIEN1MV3rRpD
                                M55RUB9UNc0RvO37d+tskROsDHTmkkHdOBmKRK9BDAcgdctC/kfbqG0FKsX6DrEeQjlZne0ezkrf
                                uVDkJtrZ88+nFLEviwn+RV96suvP8AByd03TvycwZdntYg9MzJgDB43dm6ZF3z3bVD4/vC7rR8k1
                                UxizPlKhOdQtzFy0KxEYR02PVAakrizz3OVxXfBqMvScEZbM3MutRgYeR78djY1b8mgv09/E7faQ
                                tihdD4bBA6k+ohGHqsevaUW0/f11LTqIumykbhrApwpMZyTSg2GVzi14Sen/GrTc8vRDy/T09OKv
                                mTlQMgltDqJB1WefudsTjrcwKMekEaicQcdqUgV9UwbepGtPZg==
                            </ds:X509Certificate>
                        </ds:X509Data>
                    </ds:KeyInfo>
                </ds:Signature>
            </ext:ExtensionContent>
        </ext:UBLExtension>
    </ext:UBLExtensions>
    <cbc:UBLVersionID>2.1</cbc:UBLVersionID>
    <cbc:CustomizationID>2.0</cbc:CustomizationID>
    <cbc:ID>F001-00043582</cbc:ID>
    <cbc:IssueDate>2022-01-31</cbc:IssueDate>
    <cbc:IssueTime>12:07:23</cbc:IssueTime>
    <cbc:DueDate>2022-02-28</cbc:DueDate>
    <cbc:InvoiceTypeCode listAgencyName="PE:SUNAT" listID="0101" listName="Tipo de Documento"
                         listURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo01">01
    </cbc:InvoiceTypeCode>
    <cbc:DocumentCurrencyCode listAgencyName="United Nations Economic Commission for Europe" listID="ISO 4217 Alpha"
                              listName="Currency">USD
    </cbc:DocumentCurrencyCode>
    <cbc:LineCountNumeric>1.00</cbc:LineCountNumeric>
    <cac:OrderReference>
        <cbc:ID/>
    </cac:OrderReference>
    <cac:Signature>
        <cbc:ID>F001-00043582</cbc:ID>
        <cac:SignatoryParty>
            <cac:PartyIdentification>
                <cbc:ID>20346669625</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name>CAVALI S.A. I.C.L.V.</cbc:Name>
            </cac:PartyName>
        </cac:SignatoryParty>
        <cac:DigitalSignatureAttachment>
            <cac:ExternalReference>
                <cbc:URI>#F001-00043582</cbc:URI>
            </cac:ExternalReference>
        </cac:DigitalSignatureAttachment>
    </cac:Signature>
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeAgencyName="PE:SUNAT" schemeID="6" schemeName="Documento de Identidad"
                        schemeURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo06">20346669625
                </cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name>CAVALI S.A. I.C.L.V.</cbc:Name>
            </cac:PartyName>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>CAVALI S.A. I.C.L.V.</cbc:RegistrationName>
                <cac:RegistrationAddress>
                    <cbc:ID schemeAgencyName="PE:INEI" schemeName="Ubigeos">150131</cbc:ID>
                    <cbc:AddressTypeCode listAgencyName="PE:SUNAT" listName="Establecimientos anexos">0000
                    </cbc:AddressTypeCode>
                    <cbc:CitySubdivisionName>-</cbc:CitySubdivisionName>
                    <cbc:CityName>Lima</cbc:CityName>
                    <cbc:CountrySubentity>Lima</cbc:CountrySubentity>
                    <cbc:District>San Isidro</cbc:District>
                    <cac:AddressLine>
                        <cbc:Line>AV. JORGE BASADRE GROHMANN NRO. 347 INT. 801 URB. ORRANTIA - LIMA LIMA SAN ISIDRO
                        </cbc:Line>
                    </cac:AddressLine>
                    <cac:Country>
                        <cbc:IdentificationCode listAgencyName="United Nations Economic Commission for Europe"
                                                listID="ISO 3166-1" listName="Country">PE
                        </cbc:IdentificationCode>
                    </cac:Country>
                </cac:RegistrationAddress>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingSupplierParty>
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeAgencyName="PE:SUNAT" schemeID="6" schemeName="Documento de Identidad"
                        schemeURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo06">20514733962
                </cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>ENFOCA - SOCIEDAD ADMINISTRADORA DE FONDOS DE INVERSION S.A.
                </cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingCustomerParty>
    <cac:PaymentTerms>
        <cbc:ID>FormaPago</cbc:ID>
        <cbc:PaymentMeansID>Credito</cbc:PaymentMeansID>
        <cbc:Amount currencyID="USD">118.00</cbc:Amount>
    </cac:PaymentTerms>
    <cac:PaymentTerms>
        <cbc:ID>FormaPago</cbc:ID>
        <cbc:PaymentMeansID>Cuota001</cbc:PaymentMeansID>
        <cbc:Amount currencyID="USD">118.00</cbc:Amount>
        <cbc:PaymentDueDate>2022-02-28</cbc:PaymentDueDate>
    </cac:PaymentTerms>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="USD">18.00</cbc:TaxAmount>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="USD">100.00</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="USD">18.00</cbc:TaxAmount>
            <cac:TaxCategory>
                <cac:TaxScheme>
                    <cbc:ID>1000</cbc:ID>
                    <cbc:Name>IGV</cbc:Name>
                    <cbc:TaxTypeCode>VAT</cbc:TaxTypeCode>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="USD">0.00</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="USD">0.00</cbc:TaxAmount>
            <cac:TaxCategory>
                <cac:TaxScheme>
                    <cbc:ID>9997</cbc:ID>
                    <cbc:Name>EXO</cbc:Name>
                    <cbc:TaxTypeCode>VAT</cbc:TaxTypeCode>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="USD">0.00</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="USD">0.00</cbc:TaxAmount>
            <cac:TaxCategory>
                <cac:TaxScheme>
                    <cbc:ID>9998</cbc:ID>
                    <cbc:Name>INA</cbc:Name>
                    <cbc:TaxTypeCode>FRE</cbc:TaxTypeCode>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
    </cac:TaxTotal>
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="USD">100.00</cbc:LineExtensionAmount>
        <cbc:TaxInclusiveAmount currencyID="USD">118.00</cbc:TaxInclusiveAmount>
        <cbc:PayableAmount currencyID="USD">118.00</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>
    <cac:InvoiceLine>
        <cbc:ID>1</cbc:ID>
        <cbc:InvoicedQuantity unitCode="ZZ" unitCodeListAgencyName="United Nations Economic Commission for Europe"
                              unitCodeListID="UN/ECE rec 20">1.0000000000
        </cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID="USD">100.00</cbc:LineExtensionAmount>
        <cac:PricingReference>
            <cac:AlternativeConditionPrice>
                <cbc:PriceAmount currencyID="USD">118.0000000000</cbc:PriceAmount>
                <cbc:PriceTypeCode listAgencyName="PE:SUNAT" listName="Tipo de Precio"
                                   listURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo16">01
                </cbc:PriceTypeCode>
            </cac:AlternativeConditionPrice>
        </cac:PricingReference>
        <cac:TaxTotal>
            <cbc:TaxAmount currencyID="USD">18.00</cbc:TaxAmount>
            <cac:TaxSubtotal>
                <cbc:TaxableAmount currencyID="USD">100.00</cbc:TaxableAmount>
                <cbc:TaxAmount currencyID="USD">18.00</cbc:TaxAmount>
                <cac:TaxCategory>
                    <cbc:Percent>18.00</cbc:Percent>
                    <cbc:TaxExemptionReasonCode listAgencyName="PE:SUNAT" listName="Afectacion del IGV"
                                                listURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo07">10
                    </cbc:TaxExemptionReasonCode>
                    <cac:TaxScheme>
                        <cbc:ID schemeAgencyName="PE:SUNAT" schemeID="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo05"
                                schemeName="Codigo de tributos">1000
                        </cbc:ID>
                        <cbc:Name>IGV</cbc:Name>
                        <cbc:TaxTypeCode>VAT</cbc:TaxTypeCode>
                    </cac:TaxScheme>
                </cac:TaxCategory>
            </cac:TaxSubtotal>
        </cac:TaxTotal>
        <cac:Item>
            <cbc:Description>TARIFA BASICA ENERO-2022 ENFDSR1 79010FI3</cbc:Description>
            <cac:SellersItemIdentification>
                <cbc:ID>018</cbc:ID>
            </cac:SellersItemIdentification>
            <cac:CommodityClassification>
                <cbc:ItemClassificationCode listAgencyName="GS1 US" listID="UNSPSC" listName="Item Classification">
                    78131601
                </cbc:ItemClassificationCode>
            </cac:CommodityClassification>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID="USD">100.0000000000</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>
</Invoice>
               """)

        xml_data = self.xml_string_to_dom_xml(obj)
        data_serie = xml_data.getElementsByTagName("cac:Signature")[0].getElementsByTagName("cbc:ID")[0]

        # Create provider
        provider_node = xml_data.getElementsByTagName("cac:SignatoryParty")[0]
        ruc_provider = provider_node.getElementsByTagName("cbc:ID")[0].firstChild.data
        provider_data = {
            'name': ruc_provider,
            'company_type': 'company',
            'l10n_latam_identification_type_id': 4,  # RUC
            'vat': ruc_provider
        }
        provider = self.create_model_registry_if_not_exists('res.partner', 'vat', ruc_provider, provider_data)

        # Create account move line (Detalle de factura)
        account_move_lines = []
        details = xml_data.getElementsByTagName("cac:InvoiceLine")
        for detail in details:
            # Create product
            data_producto = detail.getElementsByTagName("cac:Item")[0]
            product_name = data_producto.getElementsByTagName("cbc:Description")[0].firstChild.data
            product_data = {
                'name': product_name,
                'barcode': product_name,
                'default_code': product_name,
                'type': 'product',  # consumible?
            }
            product = self.create_model_registry_if_not_exists('product.template', 'barcode', product_name, product_data)

            # Complete detail data
            data_quantity_node = detail.getElementsByTagName("cbc:InvoicedQuantity")[0]
            quantity = data_quantity_node.firstChild.data
            unit_price = detail.getElementsByTagName("cac:Price")[0].getElementsByTagName("cbc:PriceAmount")[0].firstChild.data
            detail_data = (0, 0, {
                "product_id": product.id,
                'product_uom_id': product.uom_id.id,
                "name": product_name,
                "quantity": quantity,
                "price_unit": unit_price,
                'tax_ids': [(6, 0, self.tax_ids.ids)],
                #'account_id': self.account_id.id,
            })
            account_move_lines.append(detail_data)

        # Create account move (Factura de compra)
        invoice_date = xml_data.getElementsByTagName("cbc:IssueDate")[0].firstChild.data
        currency = xml_data.getElementsByTagName("cbc:DocumentCurrencyCode")[0].firstChild.data
        currency_odoo = self.env["res.currency"].search([("name", "=", currency)], limit=1)
        document_type = self.env["l10n_latam.document.type"].search([("name", "=", "Factura")], limit=1)
        data_serie = xml_data.getElementsByTagName("cac:Signature")[0].getElementsByTagName("cbc:ID")[0]
        serie_correlativo = data_serie.firstChild.data

        account_move_data = {
            'invoice_user_id': self.env.user.id,
            'partner_id': provider.id,
            'company_id': self.company_id.id,
            'invoice_date': invoice_date,
            'move_type': 'in_invoice',
            # "invoice_supplier_import_id": self.id,
            'currency_id': currency_odoo.id,
            'l10n_latam_document_type_id': document_type.id,  # Ruc,
            'ref': serie_correlativo,
            # "data_xml": archivo_binario,
            # "datas_fname": nombre_binario,
            # "data_pdf": pdf_binary,
            # "datas_fname_pdf": nombre_pdf,
            'invoice_line_ids': account_move_lines
        }

        invoice_id = self.env['account.move'].create(account_move_data)
        invoice_id._onchange_invoice_line_ids()
        invoice_id.invoice_line_ids._onchange_account_id()
        invoice_id.invoice_line_ids._onchange_price_subtotal()
        return "aaa"
