# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class CoffinSeasonXlsx(ReportXlsx):

    count = 1

    def generate_xlsx_report(self, workbook, data, env):
        sheet = workbook.add_worksheet()

        sheet.write(0, 0, u'日期')
        sheet.write(0, 1, u'受施亡者')
        sheet.write(0, 2, u'亡者住址')
        sheet.write(0, 3, u'領款者')
        sheet.write(0, 4, u'領款者身分字號')
        sheet.write(0, 5, u'處理者')
        sheet.write(0, 6, u'捐款者')

        for line in env:
            sheet.write(self.count, 0, line.coffin_date)
            sheet.write(self.count, 1, line.user)
            sheet.write(self.count, 2, line.con_addr)
            sheet.write(self.count, 3, line.geter)
            sheet.write(self.count, 4, line.geter_iden)
            sheet.write(self.count, 5, line.dealer)
            sheet.write(self.count, 6, line.donor)
            self.count += 1

        sheet.set_column(0, 1, 12)
        sheet.set_column(2, 2, 45)
        sheet.set_column(3, 3, 12)
        sheet.set_column(4, 4, 15)
        sheet.set_column(5, 5, 30)

        self.count = 1

CoffinSeasonXlsx('report.cdg_base.coffin_season.xlsx', 'coffin.base')