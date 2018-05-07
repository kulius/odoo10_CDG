# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class BridgeDataXlsx(ReportXlsx):

    def generate_xlsx_report(self,workbook, datas, env):

        data_num = 1

        sheet = workbook.add_worksheet(u'橋梁資料')

        sheet.write(0, 0, u'序號')
        sheet.write(0, 1, u'橋梁名稱')
        sheet.write(0, 2, u'國歷動土日期')
        sheet.write(0, 3, u'國歷謝土日期')

        for data in env:
            sheet.write(data_num, 0, data.bridge_code)
            sheet.write(data_num, 1, data.name)
            sheet.write(data_num, 2, data.build_date)
            sheet.write(data_num, 3, data.completed_date)
            data_num += 1







BridgeDataXlsx('report.cdg_base.bridge_data.xlsx', 'bridge.data')