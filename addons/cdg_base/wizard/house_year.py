# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import *
import logging


class HouseYear(models.TransientModel):
    _name = 'house.year'

    report_year = fields.Integer(string='年度收據', required=True, default=lambda r: int(datetime.today().year)-1)

    # 呼叫報表
    def call_print_report(self):
        datas = {
            'report_year': self.report_year,
        }
        return self.env['report'].get_action([], 'cdg_base.house_year', datas)


