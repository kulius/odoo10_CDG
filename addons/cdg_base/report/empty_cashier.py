# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class ReportEmptyCashier(models.AbstractModel):
    _name = 'report.cdg_base.receipt_empty_template'

    @api.multi
    def render_html(self,docids, data=None):
        Report = self.env['report']
        num = data['num']
        docargs = {
          'num': num
        }
        return Report.render('cdg_base.receipt_empty_template',docargs)