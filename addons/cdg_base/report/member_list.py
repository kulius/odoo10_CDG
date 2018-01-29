# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class MemberListXlsx(ReportXlsx):

    def generate_xlsx_report(self,workbook,data,env):
        sheet = workbook.add_worksheet()
        count = 1

        sheet.write(0, 0,u'年度')
        sheet.write(0, 1, u'收費日期')
        sheet.write(0, 2, u'收費編號')
        sheet.write(0, 3, u'姓名')
        sheet.write(0, 4, u'應繳金額')
        sheet.write(0, 5, u'連絡電話')
        sheet.write(0, 6, u'手機')
        sheet.write(0, 7, u'收據地址')
        sheet.write(0, 8, u'收費員')

        for line in env:
            if not line:
                continue
            else:
                sheet.write(count,0,line.year)
                sheet.write(count, 1, line.fee_date)
                sheet.write(count, 2, line.fee_code)
                sheet.write(count, 3, line.normal_p_id.name)
                sheet.write(count, 4, line.fee_payable)
                sheet.write(count, 5, line.con_phone)
                sheet.write(count, 6, line.cellphone)
                sheet.write(count, 7, line.rec_addr)
                sheet.write(count, 8, line.normal_p_id.cashier_name.name)
                count += 1

        sheet.set_column(1, 2, 12)
        sheet.set_column(5, 6, 12)
        sheet.set_column(7, 7, 40)
        sheet.set_column(8, 8, 12)

        count = 1

MemberListXlsx('report.cdg_base.member_list.xlsx', 'associatemember.fee')

