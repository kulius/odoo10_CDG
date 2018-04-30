# -*- coding: utf-8 -*-
from odoo import models, fields, api


class WizardPoorData(models.Model):
    _name = 'wizard.poor.data'

    start_date = fields.Date('核發時間-起', required=True)
    end_date = fields.Date('核發時間-訖', required=True)

    def print_poor_data(self):

            ids = self.env['poor.base'].search([('check_date', '>=', self.start_date), ('check_date', '<=', self.end_date)],order="check_date asc").ids

            docargs = {
                'docs': ids,
            }

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'cdg_base.case_data.xlsx',
                'datas': docargs
            }

