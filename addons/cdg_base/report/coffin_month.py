# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class CoffinMonthXlsx(ReportXlsx):

    count = 1

    def generate_xlsx_report(self, workbook, data, env):
        sheet = workbook.add_worksheet()

        sheet.write(0, 0, u'序號')
        sheet.write(0, 1, u'施出日期')
        sheet.write(0, 2, u'受施亡者')
        sheet.write(0, 3, u'領款者住址')
        sheet.write(0, 4, u'領款者')
        sheet.write(0, 5, u'領款者身分字號')

        for line in env:
            if line.donate_apply_price == 30000:
                sheet.write(self.count, 2, line.user)
            else:
                sheet.write(self.count, 2, line.user + u"*")
            sheet.write(self.count, 0, self.count)
            sheet.write(self.count, 1, line.coffin_date)
            sheet.write(self.count, 3, line.payee_addr)
            sheet.write(self.count, 4, line.geter)
            sheet.write(self.count, 5, line.geter_iden)
            self.count += 1

        sheet.set_column(1, 2, 12)
        sheet.set_column(3, 3, 45)
        sheet.set_column(4, 4, 12)
        sheet.set_column(5, 5, 15)

        self.count = 1


CoffinMonthXlsx('report.cdg_base.coffin_month.xlsx', 'coffin.base')