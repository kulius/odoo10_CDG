# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import *
import logging


class HouseYear(models.TransientModel):
    _name = 'house.year'

    report_year = fields.Integer(string='年度收據', required=True, default=lambda r: int(datetime.today().year)-1)
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員',default=lambda self: self.env.uid)

    # 呼叫報表
    def call_print_report(self):
        datas = {
            'report_year': self.report_year,
            'key_in_user': self.key_in_user.name
        }
        return self.env['report'].get_action([], 'cdg_base.house_year', datas)

    def print_report_personal(self):
        datas = {
            'report_year': self.report_year,
            'key_in_user': self.key_in_user.name
        }
        return self.env['report'].get_action([], 'cdg_base.house_year_personal', datas)
