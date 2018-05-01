# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging, time
from datetime import datetime

class MemberFeeOnly(models.Model):
    _name = 'associatemember.fee'
    _rec_name = 'fee_code'
    _order = 'year desc'
    _description = u'會員費管理'
    member_id = fields.Char(string='會員編號')
    member_note_code = fields.Char(string='會員名冊編號')
    year = fields.Char(string='年度')
    fee_code = fields.Char(string='收費編號',readonly =True)
    fee_payable = fields.Integer(string='應繳金額')
    fee_date = fields.Date(string='收費日期')
    cashier = fields.Many2one(comodel_name='cashier.base', string='收費員')
    clerk_id = fields.Char(string='收費員編號')
    normal_p_id = fields.Many2one(comodel_name='normal.p', string='關聯的會員')
    member_name = fields.Char(string='會員姓名', related='normal_p_id.name')
    member_code = fields.Char(string='捐款者編號', related='normal_p_id.new_coding')
    zip = fields.Char(string='收據郵遞區號', related='normal_p_id.zip')
    rec_addr = fields.Char(string='收據地址', related='normal_p_id.rec_addr')
    con_phone = fields.Char(string='連絡電話', related='normal_p_id.con_phone')
    cellphone = fields.Char(string='手機', related='normal_p_id.cellphone')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', default=lambda self: self.env.uid)
    key_in_user2 = fields.Char(string='輸入人員', related='key_in_user.name', readonly =True)
    temp_key_in_user = fields.Char(string='temp_輸入人員')

    @api.multi
    def write(self,vals):
      res_id = super(MemberFeeOnly,self).write(vals)
      self.normal_p_id.last_member_payment_date = self.fee_date
      return res_id

    @api.onchange('normal_p_id')
    def set_base_fee(self):
        basic_setting = self.env['ir.config_parameter'].search([])
        Annual_membership_fee = 0
        flag = False
        for line in basic_setting:
            if line.key == 'Annual_membership_fee':
                Annual_membership_fee = int(line.value)
            if line.key == 'First_Annual_membership_fee':
                First_Annual_membership_fee = int(line.value)
        for line in self.normal_p_id.member_pay_history:
            if line:
                self.fee_payable = Annual_membership_fee
                flag = True
                break
        if flag == False:
            self.fee_payable = First_Annual_membership_fee

        self.cashier = self.normal_p_id.cashier_name.id



    @api.onchange('fee_date')
    def set_fee_date(self):
        self.key_in_user = self.env.uid
        self.normal_p_id.last_member_payment_date = self.fee_date
        print 'YES'

        # self.normal_p_id.update({
        #     'member_pay_history':[1,self.id,{
        #         'key_in_user': self.env.uid
        #     }]
        # })


    @api.model
    def create(self, vals):
        res_id = super(MemberFeeOnly, self).create(vals)
        if res_id.year is False:
            raise ValidationError(u'請輸入繳費年度')
        elif not res_id.year is False:
            if res_id.fee_date:
                res_id.fee_code = 'F' + str(int(datetime.strptime(res_id.fee_date, '%Y-%m-%d').year) - 1911) + res_id.member_code
        return res_id