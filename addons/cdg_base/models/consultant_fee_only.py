# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
import logging, time

class ConsultantFeeOnly(models.Model):
    _name = 'consultant.fee'
    _rec_name = 'fee_code'
    _description = u'顧問費管理'

    consultant_id = fields.Char(string='舊顧問編號')
    year = fields.Char(string='年度')
    fee_code = fields.Char(string='收費編號',readonly =True)
    fee_payable = fields.Integer(string='應繳金額')
    fee_date = fields.Date(string='收費日期')
    cashier = fields.Many2one(comodel_name='cashier.base', string='收費員')
    clerk_id = fields.Char(string='收費員編號')
    normal_p_id = fields.Many2one(comodel_name='normal.p', string='關聯的顧問')
    member_code = fields.Char(string='捐款者編號', related='normal_p_id.new_coding')
    consultant_name = fields.Char(string='顧問姓名', related='normal_p_id.name')
    zip = fields.Char(string='收據郵遞區號', related='normal_p_id.zip')
    rec_addr = fields.Char(string='收據地址', related='normal_p_id.rec_addr')
    con_phone = fields.Char(string='連絡電話', related='normal_p_id.con_phone')
    cellphone = fields.Char(string='手機', related='normal_p_id.cellphone')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', default=lambda self: self.env.uid)
    key_in_user2 = fields.Char(string='輸入人員', related='key_in_user.name', readonly=True)
    temp_key_in_user = fields.Char(string='temp_輸入人員')

    @api.multi
    def write(self,vals):
        res_id = super(ConsultantFeeOnly,self).write(vals)
        self.normal_p_id.last_consultant_payment_date =  self.fee_date
        return res_id

    @api.onchange('normal_p_id')
    def set_base_fee(self):
        basic_setting = self.env['ir.config_parameter'].search([])
        Annual_consultants_fee = 0

        for line in basic_setting:
            if line.key == 'Annual_consultants_fee':
                Annual_consultants_fee = int(line.value)
        self.fee_payable = Annual_consultants_fee
        self.cashier = self.normal_p_id.cashier_name.id

    @api.onchange('fee_date')
    def set_fee_date(self):
        self.key_in_user = self.env.uid

    @api.model
    def create(self, vals):
        res_id = super(ConsultantFeeOnly, self).create(vals)
        if res_id.year == 0:
            raise ValidationError(u'請輸入繳費年度')
        elif not res_id.year is False:
            if res_id.fee_date:
                res_id.fee_code = 'K' + str(int(datetime.strptime(res_id.fee_date, '%Y-%m-%d').year) - 1911) + res_id.member_code
        return res_id