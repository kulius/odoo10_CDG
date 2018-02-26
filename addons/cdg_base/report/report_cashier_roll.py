# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class ReportCashierRollDonor(models.AbstractModel):
    _name = 'report.cdg_base.receipt_cashier_roll_donor_template'

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        num = data['block_num']
        target = self.env['normal.p'].browse(data['from_target'])


        docargs = {
            'doc_ids': docids,
            'doc_model': 'normal.p',
            'docs': target,
            'block_num': num,
        }


        return Report.render('cdg_base.receipt_cashier_roll_donor_template', docargs)

class ReportCashierRollMember(models.AbstractModel):
    _name = 'report.cdg_base.receipt_cashier_roll_member_template'

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        target = self.env['normal.p'].browse(docids)


        docargs = {
            'doc_ids': docids,
            'doc_model': 'normal.p',
            'docs': target,
        }

        return Report.render('cdg_base.receipt_cashier_roll_member_template', docargs)
class ReportCashierRollConsultant(models.AbstractModel):
    _name = 'report.cdg_base.receipt_cashier_roll_consultant_template'

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        target = self.env['normal.p'].browse(docids)


        docargs = {
            'doc_ids': docids,
            'doc_model': 'normal.p',
            'docs': target,
        }

        return Report.render('cdg_base.receipt_cashier_roll_consultant_template', docargs)