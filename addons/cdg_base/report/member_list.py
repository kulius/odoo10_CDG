# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class MemberListXlsx(ReportXlsx):
    count = 1

    def generate_xlsx_report(self,workbook,data, env):

        sheet = workbook.add_worksheet()

        sheet.write(0, 0, u'年度')
        sheet.write(0, 1, u'收費日期')
        sheet.write(0, 2, u'繳費情況')
        sheet.write(0, 3, u'收費編號')
        sheet.write(0, 4, u'姓名')
        sheet.write(0, 5, u'應繳金額')
        sheet.write(0, 6, u'連絡電話')
        sheet.write(0, 7, u'手機')
        sheet.write(0, 8, u'收據地址')
        sheet.write(0, 9, u'收費員編號')

        for line in env:
            if not line:
                pass
            else:
                if not line.fee_date:
                    sheet.write(self.count, 2, u"未繳費")
                else:
                    sheet.write(self.count, 2, u"已繳費")
                sheet.write(self.count, 0,line.year)
                sheet.write(self.count, 1, line.fee_date)
                sheet.write(self.count, 3, line.fee_code)
                sheet.write(self.count, 4, line.normal_p_id.name)
                sheet.write(self.count, 5, line.fee_payable)
                sheet.write(self.count, 6, line.con_phone)
                sheet.write(self.count, 7, line.cellphone)
                sheet.write(self.count, 8, line.rec_addr)
                sheet.write(self.count, 9, line.clerk_id)
                self.count += 1

        sheet.set_column(1, 1, 12)
        sheet.set_column(3, 3, 12)
        sheet.set_column(6, 7, 12)
        sheet.set_column(8, 8, 40)
        sheet.set_column(9, 9, 12)

        self.count = 1





MemberListXlsx('report.cdg_base.member_list.xlsx', 'associatemember.fee')

