# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class DonateTotallyXlsx(ReportXlsx):

    count = 1

    def generate_xlsx_report(self, workbook, datas, env):
        sheet = workbook.add_worksheet()

        sheet.write(0, 0, u'日期')
        sheet.write(0, 1, u'舊團員編號')
        sheet.write(0, 2, u'新捐款者編號')
        sheet.write(0, 3, u'捐款者姓名')
        sheet.write(0, 4, u'捐款總額')
        sheet.write(0, 5, u'收據地址')

        for data in datas['docs']:
            line = self.env['donate.single'].browse(data)
            sheet.write(self.count, 0, line.donate_date)
            sheet.write(self.count, 1, line.w_id)
            sheet.write(self.count, 2, line.new_coding)
            sheet.write(self.count, 3, line.name)
            sheet.write(self.count, 4, line.donate_total)
            sheet.write(self.count, 5, line.rec_addr)
            self.count += 1

        sheet.set_column(1, 2, 12)
        sheet.set_column(3, 3, 45)
        sheet.set_column(4, 4, 12)
        sheet.set_column(5, 5, 15)

        self.count = 1


DonateTotallyXlsx('report.cdg_base.donate_totally.xlsx', 'donate.single')