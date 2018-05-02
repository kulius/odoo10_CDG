# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class ReportCaseImages(models.AbstractModel):
    _name = 'report.cdg_base.receipt_case_images_template'

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        data = self.env['poor.image'].browse(data['poor_images'])
        docargs = {
            'doc_ids': docids,
            'doc_model': 'poor.image',
            'docs': data,
        }


        return Report.render('cdg_base.receipt_case_images_template', docargs)

class ReportCaseDocuments(models.AbstractModel):
    _name = 'report.cdg_base.receipt_case_documents_template'

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        data = self.env['poor.document'].browse(data['poor_documents'])
        docargs = {
            'doc_ids': docids,
            'doc_model': 'poor.document',
            'docs': data,
        }


        return Report.render('cdg_base.receipt_case_documents_template', docargs)