# -*- coding: utf-8 -*-
from odoo import models, fields, api


class WizardPoorData(models.Model):
    _name = 'wizard.poor.data'

    start_date = fields.Date('申請時間-起')
    end_date = fields.Date('申請時間-訖')

    def print_poor_data(self):

            ids = self.env['poor.base'].search([('apply_date', '>=', self.start_date), ('apply_date', '<=', self.end_date)],order="apply_date asc").ids

            docargs = {
                'docs': ids,
            }

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'cdg_base.case_data.xlsx',
                'datas': docargs
            }