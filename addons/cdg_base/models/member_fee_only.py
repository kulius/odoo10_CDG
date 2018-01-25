# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging, time
from datetime import datetime

class MemberFeeOnly(models.Model):
    _name = 'associatemember.fee'

    member_id = fields.Char(string='會員編號')
    member_note_code = fields.Char(string='會員名冊編號')
    year = fields.Char(string='年度',default=datetime.today().year - 1911)
    fee_code = fields.Char(string='收費編號')
    fee_payable = fields.Integer(string='應繳金額')
    fee_date = fields.Date(string='收費日期',default=datetime.today())
    clerk_id = fields.Char(string='收費員編號')
    normal_p_id = fields.Many2one(comodel_name='normal.p', string='關聯的會員')
    rec_addr = fields.Char(string='收據地址', related='normal_p_id.rec_addr')
    con_phone = fields.Char(string='連絡電話', related='normal_p_id.con_phone')
    cellphone = fields.Char(string='手機', related='normal_p_id.cellphone')
