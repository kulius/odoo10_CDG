# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class CashierListXlsx(ReportXlsx):

    count = 1

    def generate_xlsx_report(self,workbook,data,env):
        sheet = workbook.add_worksheet()

        format1 = workbook.add_format({'border':2})

        sheet.write(0, 0,u'捐款者編號')
        sheet.write(0, 1, u'舊團員編號')
        sheet.write(0, 2, u'姓名')
        sheet.write(0, 3, u'連絡電話')
        sheet.write(0, 4, u'手機')
        sheet.write(0, 5, u'報表寄送地址')

        for line in env:
            sheet.write(self.count, 0, line.new_coding)
            sheet.write(self.count, 1, line.old_coding)
            sheet.write(self.count, 2, line.name)
            sheet.write(self.count, 3, line.con_phone)
            sheet.write(self.count, 4, line.cellphone)
            sheet.write(self.count, 5, line.zip_code + line.con_addr)
            sheet.write(self.count, 6,'', format1)
            sheet.write(self.count, 7, '', format1)
            sheet.write(self.count, 8, '', format1)
            self.count += 1

        sheet.set_column(0, 1, 12)
        sheet.set_column(3, 4, 12)
        sheet.set_column(5, 5, 40)
        sheet.set_column(6, 8, 4)

        self.count = 1








CashierListXlsx('report.cdg_base.cashier_list.xlsx', 'normal.p')