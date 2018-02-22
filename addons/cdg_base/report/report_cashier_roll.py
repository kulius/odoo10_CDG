# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class ReportCashierRoll(models.AbstractModel):
    _name = 'report.cdg_base.receipt_cashier_roll_template'

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        target = self.env['normal.p'].browse(docids)


        docargs = {
            'doc_ids': docids,
            'doc_model': 'normal.p',
            'docs': target,
        }

        return Report.render('cdg_base.receipt_cashier_roll_template', docargs)