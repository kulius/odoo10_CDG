# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
import logging, time

class ConsultantFeeOnly(models.Model):
    _name = 'consultant.fee'

    consultant_id = fields.Char(string='舊顧問編號')
    year = fields.Char(string='年度',default=datetime.today().year - 1911)
    fee_code = fields.Char(string='收費編號')
    fee_payable = fields.Integer(string='應繳金額')
    fee_date = fields.Date(string='收費日期',default=datetime.today())
    clerk_id = fields.Char(string='收費員編號')
    normal_p_id = fields.Many2one(comodel_name='normal.p', string='關聯的顧問')
    consultant_name = fields.Char(string='顧問姓名', related='normal_p_id.name')
    rec_addr = fields.Char(string='收據地址', related='normal_p_id.rec_addr')
    con_phone = fields.Char(string='連絡電話', related='normal_p_id.con_phone')
    cellphone = fields.Char(string='手機', related='normal_p_id.cellphone')
