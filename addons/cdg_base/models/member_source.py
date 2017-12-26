# -*- coding: utf-8 -*-
import time ,datetime

# import psycopg2

from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class MemberSource(models.Model):
    _name = "member.source"

    member_code = fields.Char('舊會員編號')
    member_id = fields.Char('會員編號')
    type = fields.Many2many(comodel_name='people.type', string='人員種類')
    name = fields.Char(string='姓名')
    self_iden = fields.Char(string='身分證字號') #大多為空
    birth = fields.Date(string='生日')
    cellphone = fields.Char(string='手機')
    con_phone = fields.Char(string='連絡電話(一)')
    con_phone2 = fields.Char(string='連絡電話(二)')

    zip1 = fields.Char() #戶籍地址的zip
    rec_addr = fields.Char(string='戶籍地址')
    zip2 = fields.Char() #通訊地址的zip
    con_addr = fields.Char(string='通訊地址')
    build_date = fields.Date(string='建檔日期')
    ps = fields.Text(string='備註')
    cashier_code = fields.Many2one(comodel_name='c.worker', string='收費員編號') # M2o c.worker
    rec_send = fields.Boolean(string='收據寄送')
    booklist = fields.Boolean(string='名冊列印')
    sequence = fields.Char(string='排序')
    key_in_user = fields.Many2one(comodel_name='c.worker', string='輸入人員', ondelete='cascade') # 原來的直接貼上
    db_chang_date = fields.Date(string='異動日期')