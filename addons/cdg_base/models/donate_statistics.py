# -*- coding: utf-8 -*-

from odoo import models, fields, api

class donatestatistics(models.Model):
    _name = "donate.statistics"

    year = fields.Char(string='捐款年度')
    month = fields.Char(string='捐款月份')
    households = fields.Integer(string='捐款戶數')
    receipt_number = fields.Integer(string='收據張數')
    number = fields.Integer(string='總捐款人數')
    number_of_people = fields.Integer(string='實際捐款人數')
    type = fields.Char(string='種類')

