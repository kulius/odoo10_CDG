# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class CashierListXlsx(ReportXlsx):

    count = 2

    def generate_xlsx_report(self,workbook,data,env):
        sheet = workbook.add_worksheet()

        sheet.write(1, 1,u'捐款者編號')
        sheet.write(1, 2, u'舊團員編號')
        sheet.write(1, 3, u'姓名')
        sheet.write(1, 4, u'連絡電話')
        sheet.write(1, 5, u'手機')
        sheet.write(1, 6, u'報表寄送地址')

        for line in env:
            sheet.write(self.count,1,line.new_coding)
            sheet.write(self.count, 2, line.old_coding)
            sheet.write(self.count, 3, line.name)
            sheet.write(self.count, 4, line.con_phone)
            sheet.write(self.count, 5, line.cellphone)
            sheet.write(self.count, 6, line.con_addr)
            self.count += 1

        sheet.set_column(1, 2, 12)
        sheet.set_column(4, 5, 12)
        sheet.set_column(6, 6, 40)





CashierListXlsx('report.cdg_base.cashier_list.xlsx', 'normal.p')