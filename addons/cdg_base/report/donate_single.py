# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ReportDonateSingle(models.AbstractModel):
    _name = 'report.cdg_base.receipt_single_all_template'

    name = fields.Char()

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        target = self.env['donate.single'].browse(docids)
        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.single',
            'docs': target.donate_list,
            'data': target,
        }
        return Report.render('cdg_base.receipt_single_all_template', docargs)


class ReportDonateSingleIndependent(models.AbstractModel):
    _name = 'report.cdg_base.receipt_single_independent_template'

    name = fields.Char()

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        target = self.env['donate.single'].browse(docids)
        boss = 0
        for line in target.donate_list:
            if line.donate_member.number == '1':
                boss = line.donate_member
                break

        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.batch',
            'docs': target.donate_list,
            'boss': boss.donate_family1,
        }
        return Report.render('cdg_base.receipt_single_independent_template', docargs)