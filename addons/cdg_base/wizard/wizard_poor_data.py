# -*- coding: utf-8 -*-
from odoo import models, fields, api


class WizardPoorData(models.TransientModel):
    _name = 'wizard.poor.data'

    start_date = fields.Date('領款時間-起', required=True)
    end_date = fields.Date('領款時間-訖', required=True)

    def print_poor_data(self):

            ids = self.env['poor.base'].search([('last_receive_time', '>=', self.start_date), ('last_receive_time', '<=', self.end_date)],order="last_receive_time asc").ids

            docargs = {
                'docs': ids,
            }

            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'cdg_base.case_data.xlsx',
                'datas': docargs
            }

