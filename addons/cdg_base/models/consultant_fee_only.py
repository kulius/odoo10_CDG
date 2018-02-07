# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
import logging, time

class ConsultantFeeOnly(models.Model):
    _name = 'consultant.fee'
    _rec_name = 'fee_code'

    consultant_id = fields.Char(string='舊顧問編號')
    year = fields.Integer(string='年度',default= int(datetime.today().year - 1911))
    fee_code = fields.Char(string='收費編號')
    fee_payable = fields.Integer(string='應繳金額')
    fee_date = fields.Date(string='收費日期',default=datetime.today())
    cashier = fields.Many2one(comodel_name='cashier.base', string='收費員')
    clerk_id = fields.Char(string='收費員編號')
    normal_p_id = fields.Many2one(comodel_name='normal.p', string='關聯的顧問')
    consultant_name = fields.Char(string='顧問姓名', related='normal_p_id.name')
    rec_addr = fields.Char(string='收據地址', related='normal_p_id.rec_addr')
    con_phone = fields.Char(string='連絡電話', related='normal_p_id.con_phone')
    cellphone = fields.Char(string='手機', related='normal_p_id.cellphone')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', states={2: [('readonly', True)]},default=lambda self: self.env.uid)
    temp_key_in_user = fields.Char(string='temp_輸入人員')

    @api.onchange('normal_p_id')
    def set_base_fee(self):
        basic_setting = self.env['ir.config_parameter'].search([])
        Annual_consultants_fee = 0

        for line in basic_setting:
            if line.key == 'Annual_consultants_fee':
                Annual_consultants_fee = int(line.value)
        self.fee_payable = Annual_consultants_fee
