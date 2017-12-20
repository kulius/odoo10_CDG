# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging, time

class MemberFeeOnly(models.Model):
    _name = 'member.only.fee'

    member_id = fields.Char(string='舊會員編號')
    member_note_code = fields.Char(string='會員名冊編號')
    year = fields.Char(string='年度')
    fee_code = fields.Char(string='收費編號')
    fee_payable = fields.Integer(string='應繳金額')
    fee_date = fields.Date(string='收費日期')
    clerk_id = fields.Char(string='收費員編號')
    normal_p_id = fields.Many2one(comodel_name='normal.p', string='關聯的會員')
