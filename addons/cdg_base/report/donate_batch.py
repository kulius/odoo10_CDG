# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ReportDonateBatch(models.AbstractModel):
    _name = 'report.cdg_base.receipt_all_template'

    name = fields.Char()

    @api.model
    def render_html(self, docids, data=None):

        Report = self.env['report']
        target = self.env['donate.batch'].browse(docids)


        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.batch',
            'docs': target.donate_list,
            'data': target,
        }
        return Report.render('cdg_base.receipt_all_template', docargs)


class ReportDonateBatchIndependent(models.AbstractModel):
    _name = 'report.cdg_base.receipt_independent_template'

    name = fields.Char()

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        target = self.env['donate.batch'].browse(docids)



        boss = 0
        for line in target.donate_list:
            if line.donate_user.number == '1':
                boss = line.donate_user
                break

        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.batch',
            'docs': target.donate_list,
            'boss': boss.donate_family1,
        }
        return Report.render('cdg_base.receipt_independent_template', docargs)
