# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo import models, fields, api

class PoorBase(models.Model):
    _name = 'poor.base'

    name = fields.Char('姓名')
    self_iden = fields.Char('身分證號')
    case_id = fields.Char('案件編號')
    allow_money = fields.Integer('申請費用')
    receive_money = fields.Integer('已領金額')
    zip = fields.Char(string='收據郵遞區號')
    rec_addr = fields.Char(string='收據寄送地址')
    zip_code = fields.Char(string='報表郵遞區號')
    con_addr = fields.Char(string='報表寄送地址')
    case_date = fields.Date('案件日期',default=datetime.today())

    @api.model
    def create(self, vals):
        res_id = super(PoorBase, self).create(vals)

        if res_id.name is False or res_id.self_iden is False:
            raise ValidationError('姓名或身分證號不能為空白')
        else:
            res_id.case_id = res_id.case_date[0:4] + res_id.case_date.split('-')[1]

        return res_id

