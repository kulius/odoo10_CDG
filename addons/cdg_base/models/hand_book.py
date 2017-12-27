# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HandChecking(models.Model):

    _name = "hand.checking"

    book_code = fields.Char('簿冊編號')
    name = fields.Char('領取人')
    take_date = fields.Date('領取日期') #原始資料為Char
    recycle_date = fields.Date('回收日期') #原始資料為Char
    recycle_money = fields.Float('已收總金額')
    build_date = fields.Date('建檔日期') #原始資料為Char
    ps = fields.Text('備註')
    key_in_user = fields.Many2one(comodel_name='c.worker',string='輸入人員', ondelete='cascade')
    db_chang_date = fields.Date(string='異動日期') #原始資料為Char