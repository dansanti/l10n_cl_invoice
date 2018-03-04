# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
import re


class res_partner(models.Model):
    _inherit = 'res.partner'

    def _get_default_tp_type(self):
        try:
            return self.env.ref('l10n_cl_invoice.res_IVARI')
        except:
            return self.env['sii.responsability']

    def _get_default_doc_type(self):
        try:
            return self.env.ref('l10n_cl_invoice.dt_RUT')
        except:
            return self.env['sii.document_type']

    responsability_id = fields.Many2one(
        'sii.responsability',
        string='Responsability',
        default=lambda self: self._get_default_tp_type(),
    )
    document_type_id = fields.Many2one(
        'sii.document_type',
        string='Document type',
        default=lambda self: self._get_default_doc_type(),
    )
    document_number = fields.Char(
        string='Document number',
        size=64,
    )
    start_date = fields.Date(
        string='Start-up Date',
    )
    tp_sii_code = fields.Char(
        'Tax Payer SII Code',
        compute='_get_tp_sii_code',
        readonly=True,
    )

    @api.multi
    @api.onchange('responsability_id')
    def _get_tp_sii_code(self):
        for record in self:
            record.tp_sii_code=str(record.responsability_id.tp_sii_code)

    @api.onchange('document_number', 'document_type_id')
    def onchange_document(self):
        mod_obj = self.env['ir.model.data']
        if self.document_number and ((
            'sii.document_type',
            self.document_type_id.id) == mod_obj.get_object_reference(
                'l10n_cl_invoice', 'dt_RUT') or ('sii.document_type',
                self.document_type_id.id) == mod_obj.get_object_reference(
                    'l10n_cl_invoice', 'dt_RUN')):
            document_number = (
                re.sub('[^1234567890Kk]', '', str(
                    self.document_number))).zfill(9).upper()
            vat = 'CL%s' % document_number
            exist = self.env['res.partner'].search(
                [
                    ('vat','=', vat),
                    ('vat', '!=',  'CL555555555'),
                ],
                limit=1,
            )
            if exist:
                self.vat = ''
                self.document_number = ''
                return {
                    'warning': {
                        'title': "El Rut ya está siendo usado",
                        'message': _("El usuario %s está utilizando este documento" ) % exist.name,
                        }
                    }
            self.vat = vat
            self.document_number = '%s.%s.%s-%s' % (
                                        document_number[0:2], document_number[2:5],
                                        document_number[5:8], document_number[-1],
                                    )
        elif self.document_number and (
            'sii.document_type',
            self.document_type_id.id) == mod_obj.get_object_reference(
                'l10n_cl_invoice',
                'dt_Sigd',
            ):
            self.document_number = ''
        else:
            self.vat = ''
