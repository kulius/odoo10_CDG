# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class CaseDataXlsx(ReportXlsx):

    def generate_xlsx_report(self,workbook, datas, env):
        case_data = self.env['poor.base'].browse(datas['docs'])

        sheet = workbook.add_worksheet(u'貧困扶助季表')
        sheet.write(0, 0, u'案件編號')
        sheet.write(0, 1, u'案主姓名')
        sheet.write(0, 2, u'單次金額')
        sheet.write(0, 3, u'單次時間')
        sheet.write(0, 4, u'第一期')
        sheet.write(0, 5, u'第二期')
        sheet.write(0, 6, u'第三期')
        sheet.write(0, 7, u'申請總額')
        sheet.write(0, 8, u'通訊地址')
        sheet.write(0, 9, u'案主身分證號')

        for data in case_data:
            data_count = 1
            data_time = 1
            sheet.write(data_count, 0, data.case_id)
            sheet.write(data_count, 1, data.name)
            sheet.write(data_count, 2, data.once_money)
            sheet.write(data_count, 7, data.allow_money)
            sheet.write(data_count, 8, data.mail_addr)
            sheet.write(data_count, 9, data.self_iden)
            sheet.set_column(0, 6, 10)
            sheet.set_column(8, 8, 25)
            sheet.set_column(9, 9, 13)
            for data_rec in case_data.poor_receive:
               if len(case_data.poor_receive) == 1:
                   sheet.write(data_count, 3,data_rec.receive_date)
               elif len(case_data.poor_receive) == 2:
                   if  data_time == 1:
                       sheet.write(data_count, 4, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 2:
                       sheet.write(data_count, 5, data_rec.receive_date)
               elif len(case_data.poor_receive) == 3:
                   if data_time == 1:
                       sheet.write(data_count, 4, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 2:
                       sheet.write(data_count, 5, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 3:
                       sheet.write(data_count, 6, data_rec.receive_date)
                       data_time += 1
               elif len(case_data.poor_receive) == 4:
                   if data_time == 1:
                       sheet.write(data_count, 4, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 2:
                       sheet.write(data_count, 5, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 3:
                       sheet.write(data_count, 6, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 4:
                       data_count += 1
                       sheet.write(data_count, 4, data_rec.receive_date)
                       data_time += 1
               elif len(case_data.poor_receive) == 5:
                   if data_time == 1:
                       sheet.write(data_count, 4, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 2:
                       sheet.write(data_count, 5, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 3:
                       sheet.write(data_count, 6, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 4:
                       data_count += 1
                       sheet.write(data_count, 4, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 5:
                       sheet.write(data_count, 5, data_rec.receive_date)
                       data_time += 1
               elif len(case_data.poor_receive) == 6:
                   if data_time == 1:
                       sheet.write(data_count, 4, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 2:
                       sheet.write(data_count, 5, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 3:
                       sheet.write(data_count, 6, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 4:
                       data_count += 1
                       sheet.write(data_count, 4, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 5:
                       sheet.write(data_count, 5, data_rec.receive_date)
                       data_time += 1
                   elif data_time == 6:
                       sheet.write(data_count, 6, data_rec.receive_date)





CaseDataXlsx('report.cdg_base.case_data.xlsx', 'normal.p')