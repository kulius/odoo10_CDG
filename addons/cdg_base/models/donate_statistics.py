# -*- coding: utf-8 -*-

from odoo import models, fields, api

class donatestatistics(models.Model):
    _name = "donate.statistics"

    year = fields.Char(string='捐款年度')
    month = fields.Char(string='捐款月份')
    households = fields.Integer(string='捐款戶數')
    number = fields.Integer(string='捐款人數')
