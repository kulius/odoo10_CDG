# -*- coding: utf-8 -*-
import time ,datetime
# import psycopg2

from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class ConsultantSource(models.Model):
    _name = 'consultant.source'

    consultant_code = fields.Char("舊顧問編號")
    consultant_id = fields.Char('顧問編號')
    type = fields.Char(string='人員種類')  # 人 種類
    name = fields.Char(string='姓名')
    birth = fields.Date(string='生日')
    cellphone = fields.Char(string='手機')
    con_phone = fields.Char(string='連絡電話(一)')
    con_phone2 = fields.Char(string='連絡電話(二)')

    zip1 = fields.Char() #收據地址的zip
    rec_addr = fields.Char(string='收據地址')
    zip2 = fields.Char() #聯絡地址的zip
    con_addr = fields.Char(string='聯絡地址')
    hire_date = fields.Char(string='聘顧日期')
    build_date = fields.Date(string='建檔日期')
    ps = fields.Text(string='備註')
    cashier_code = fields.Char(string='收費員編號')  # M2o c.worker
    rec_send = fields.Boolean(string='收據寄送')
    report_send = fields.Boolean(string='報表寄送')
    thanks_send = fields.Boolean(string='感謝狀寄送')
    sequence = fields.Integer(string='排序')
    key_in_user = fields.Many2one(comodel_name='c.worker', string='輸入人員', ondelete='cascade') # 原來的直接貼上
    db_chang_date = fields.Date(string='異動日期')