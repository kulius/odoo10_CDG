# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class DonateOrderXlsx(ReportXlsx):
    count = 1

    def generate_xlsx_report(self, workbook, data, env):
        sheet = workbook.add_worksheet()

        sheet.write(0, 0, u'捐款者編號')
        sheet.write(0, 1, u'捐款者姓名')
        sheet.write(0, 2, u'捐款金額')
        sheet.write(0, 3, u'捐款總額')
        sheet.write(0, 4, u'捐款項目')
        sheet.write(0, 5, u'捐款日期')
        sheet.write(0, 6, u'收費員')

        for line in env:
            if not line:
                continue
            else:
                sheet.write(self.count, 0, line.donate_new_coding)
                sheet.write(self.count, 1, line.donate_member.name)
                sheet.write(self.count, 2, line.donate)
                sheet.write(self.count, 3, line.donate_total)
                if line.donate_type == 1:
                    sheet.write(self.count, 4, u"造橋")
                elif line.donate_type == 2:
                    sheet.write(self.count, 4, u"鋪路")
                elif line.donate_type == 3:
                    sheet.write(self.count, 4, u"施棺")
                elif line.donate_type == 5:
                    sheet.write(self.count, 4, u"伙食費")
                elif line.donate_type == 5:
                    sheet.write(self.count, 4, u"貧困扶助")
                elif line.donate_type == 6:
                    sheet.write(self.count, 4, u"不指定")
                elif line.donate_type == 99:
                    sheet.write(self.count, 4, u"其他工程")
                sheet.write(self.count, 5, line.donate_date)
                sheet.write(self.count, 6, line.donate_member.cashier_name.name)
                self.count += 1

        sheet.set_column(0, 1, 12)
        sheet.set_column(5,6,12)

        self.count = 1



DonateOrderXlsx('report.cdg_base.donate_order.xlsx', 'donate.order')