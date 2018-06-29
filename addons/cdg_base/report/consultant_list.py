# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class ConsultantListXlsx(ReportXlsx):



    def generate_xlsx_report(self,workbook,data,env):

        array = self.env['consultant.fee']
        sheet = workbook.add_worksheet()
        count = 1

        sheet.write(0, 0, u'顧問編號')
        sheet.write(0, 1, u'姓名')
        sheet.write(0, 2, u'收據地址')
        sheet.write(0, 3, u'顧問加入日期')

        for line in data['docs']:
            data = array.browse(line)
            if not data:
                continue
            else:
                sheet.write(count, 0, data.member_code)
                sheet.write(count, 1, data.consultant_name)
                sheet.write(count, 2, data.rec_addr)
                sheet.write(count, 3, data.normal_p_id.hire_date)
                count += 1



        count = 1



ConsultantListXlsx('report.cdg_base.consultant_list.xlsx', 'consultant.fee')