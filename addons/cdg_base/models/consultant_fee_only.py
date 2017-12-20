# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging, time

class ConsultantFeeOnly(models.Model):
    _name = 'consultant.fee'

    consultant_id = fields.Char(string='舊顧問編號')
    year = fields.Char(string='年度')
    fee_code = fields.Char(string='收費編號')
    fee_payable = fields.Integer(string='應繳金額')
    fee_date = fields.Date(string='收費日期')
    clerk_id = fields.Char(string='收費員編號')
    normal_p_id = fields.Many2one(comodel_name='normal.p', string='關聯的顧問')
