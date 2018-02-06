# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class CoffinSeasonXlsx(ReportXlsx):

    count = 2
    coffin_count = 1

    def generate_xlsx_report(self, workbook, data, env):
        sheet = workbook.add_worksheet()
        sheet.write(1, 0, u'序號')
        sheet.write(1, 1, u'死亡日期')
        sheet.write(1, 2, u'受施亡者')
        sheet.write(1, 3, u'亡者住址')
        sheet.write(1, 4, u'領款者')
        sheet.write(1, 5, u'處理者')
        sheet.write(1, 6, u'捐款者')

        for line in env:
            if line.donate_apply_price == 30000:
                sheet.write(self.count, 2, line.user)
            else:
                sheet.write(self.count, 2, line.user + u"*")
            sheet.write(self.count, 0, self.coffin_count)
            sheet.write(self.count, 1, line.dead_date)
            sheet.write(self.count, 3, line.con_addr)
            sheet.write(self.count, 4, line.geter)
            sheet.write(self.count, 5, line.dealer)
            sheet.write(self.count, 6, line.donor)
            self.count += 1
            self.coffin_count += 1

        sheet.set_column(0, 0, 11)
        sheet.set_column(1, 2, 12)
        sheet.set_column(3, 3, 45)
        sheet.set_column(4, 4, 12)
        sheet.set_column(5, 5, 15)
        sheet.set_column(6, 6, 30)
        sheet.write(0,0,u'施棺總筆數')
        sheet.write(0,1,self.coffin_count-1)
        sheet.write(0,2,u'筆')

        self.count = 2
        self.coffin_count = 1

CoffinSeasonXlsx('report.cdg_base.coffin_season.xlsx', 'coffin.base')