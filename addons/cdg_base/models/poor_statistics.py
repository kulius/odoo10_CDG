# -*- coding: utf-8 -*-

from odoo import models, fields, api

class donatestatistics(models.Model):
    _name = "poor.statistics"

    year = fields.Char(string='捐款年度')
    month = fields.Char(string='捐款月份')
    case_number = fields.Integer(string='案件數')

