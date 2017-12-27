# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CashierBase(models.Model):
    _name = 'cashier.base'

    c_id = fields.Char(string='收費員編號')
    name = fields.Char(string='收費員姓名')
    build_date = fields.Date(string='建檔日期')

    self_iden = fields.Char(string='身分證字號')
    con_phone = fields.Char(string='聯絡電話(一)')
    con_phone2 = fields.Char(string='聯絡電話(二)')
    cellphone = fields.Char(string='手機')
    con_addr = fields.Char(string='通訊地址')
    ps = fields.Text(string='備註')

    normal_cash = fields.Many2many(comodel_name='normal.p',string='捐款人繳費名冊')
    member_cash = fields.Many2many(comodel_name='normal.p',string='會員繳費名冊')
    consultant_cash = fields.Many2many(comodel_name='normal.p',string='顧問繳費名冊')
