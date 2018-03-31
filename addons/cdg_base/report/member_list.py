# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class MemberListXlsx(ReportXlsx):


    def generate_xlsx_report(self,workbook,data,env):

        array = self.env['associatemember.fee']
        sheet = workbook.add_worksheet()
        count = 1

        sheet.write(0, 0,u'會員編號')
        sheet.write(0, 1, u'姓名')
        sheet.write(0, 2, u'收據地址')

        for line in data['docs']:
            data = array.browse(line)
            if not data:
                continue
            else:
                sheet.write(count, 0, data.member_code)
                sheet.write(count, 1, data.member_name)
                sheet.write(count, 2, data.rec_addr)
                count += 1

        # sheet.set_column(1, 1, 12)
        # sheet.set_column(3, 3, 12)
        # sheet.set_column(6, 7, 12)
        # sheet.set_column(8, 8, 40)
        # sheet.set_column(9, 9, 12)

        count = 1

MemberListXlsx('report.cdg_base.member_list.xlsx', 'associatemember.fee')

