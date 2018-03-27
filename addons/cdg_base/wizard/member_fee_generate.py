# -*- coding: utf-8 -*-
from odoo import models, fields, api

class memnberfeegenerate(models.Model):
    _name = 'memnber.fee.generate'
    _description = u'會員費產生'

    year = fields.Char(string='繳費年度')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', default=lambda self: self.env.uid)

    def start_member_batch(self):
        basic_setting = self.env['ir.config_parameter'].search([])
        Annual_membership_fee = 0
        for line in basic_setting:
            if line.key == 'Annual_membership_fee':
                Annual_membership_fee = int(line.value)
        if len(self.year) == 4:
            self.year = str(int(self.year) - 1911)

        data_line = []
        temp = []
        normal_p_members = self.env['normal.p'].search(['|',('type.id','=',2),('type.id','=',3)]).ids
        member_fee_datas = self.env['associatemember.fee'].search([('year','=',self.year)])
        for line in member_fee_datas:
            temp.append(line.normal_p_id.id)

        data_line = list(set(normal_p_members) - set(temp))
        target = self.env['normal.p'].browse(data_line)
        for line in target:
            self.env['associatemember.fee'].create({
                'year':self.year,
                'fee_code': 'F' + str(self.year) + str(line.new_coding),
                'fee_payable':Annual_membership_fee,
                'normal_p_id': line.id,
                'cashier':line.cashier_name.id,
                'key_in_user': self.key_in_user.id
            })
        return True
