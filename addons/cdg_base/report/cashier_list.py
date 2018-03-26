# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class CashierListXlsx(ReportXlsx):


    def generate_xlsx_report(self,workbook, datas, env):
        data_count = 1
        zip = 0


        donor_data = self.env['normal.p'].browse(datas['docs'])

        for data in donor_data:

            if zip != data.postal_code_id.zip:
                data_count = 1
                zip = data.postal_code_id.zip
                sheet = workbook.add_worksheet(zip + data.postal_code_id.city)
                sheet.write(0, 0,u'捐款者編號')
                sheet.write(0, 1, u'舊團員編號')
                sheet.write(0, 2, u'姓名')
                sheet.write(0, 3, u'連絡電話')
                sheet.write(0, 4, u'手機')
                sheet.write(0, 5, u'報表寄送地址')
            sheet.write(data_count, 0, data.new_coding)
            sheet.write(data_count, 1, data.w_id)
            sheet.write(data_count, 2, data.name)
            sheet.write(data_count, 3, data.con_phone)
            sheet.write(data_count, 4, data.cellphone)
            sheet.write(data_count, 5, data.zip_code + data.con_addr)
            data_count += 1


CashierListXlsx('report.cdg_base.cashier_list.xlsx', 'normal.p')