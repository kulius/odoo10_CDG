# -*- coding: utf-8 -*-
import itertools
from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class CaseDataXlsx(ReportXlsx):

    def generate_xlsx_report(self,workbook, datas, env):
        case_data = self.env['poor.base'].browse(datas['docs'])


CaseDataXlsx('report.cdg_base.case_data.xlsx', 'normal.p')