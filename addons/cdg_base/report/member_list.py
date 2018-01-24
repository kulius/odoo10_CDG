# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class MemberListXlsx(ReportXlsx):

    count = 2

    def generate_xlsx_report(self,workbook,data,env):
        sheet = workbook.add_worksheet()

        sheet.write(1, 1,u'年度')
        sheet.write(1, 2, u'收費日期')
        sheet.write(1, 3, u'收費編號')
        sheet.write(1, 4, u'姓名')
        sheet.write(1, 5, u'應繳金額')
        sheet.write(1, 6, u'連絡電話')
        sheet.write(1, 7, u'手機')
        sheet.write(1, 8, u'收據地址')
        sheet.write(1, 9, u'收費員編號')


        for line in env:
            sheet.write(self.count,1,line.year)
            sheet.write(self.count, 2, line.fee_date)
            sheet.write(self.count, 3, line.fee_code)
            sheet.write(self.count, 4, line.normal_p_id.name)
            sheet.write(self.count, 5, line.fee_payable)
            sheet.write(self.count, 6, line.con_phone)
            sheet.write(self.count, 7, line.cellphone)
            sheet.write(self.count, 8, line.rec_addr)
            sheet.write(self.count, 9, line.clerk_id)
            self.count += 1

        sheet.set_column(2, 3, 12)
        sheet.set_column(6, 7, 12)
        sheet.set_column(8, 8, 40)
        sheet.set_column(9, 9, 12)





MemberListXlsx('report.cdg_base.member_list.xlsx', 'associatemember.fee')