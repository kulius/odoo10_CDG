# -*- coding: utf-8 -*-
from odoo import models, fields, api

class consultantfeegenerate(models.Model):
    _name = 'consultant.fee.generate'
    _description = u'顧問費產生'

    year = fields.Char(string='繳費年度')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員',default=lambda self: self.env.uid)

    def start_consultant_batch(self):
        basic_setting = self.env['ir.config_parameter'].search([])
        Annual_consultants_fee = 0
        for line in basic_setting:
            if line.key == 'Annual_consultants_fee':
                Annual_consultants_fee = int(line.value)
        if len(self.year) == 4:
            self.year = str(int(self.year) - 1911)

        data_line = []
        temp = []
        normal_p_consultants = self.env['normal.p'].search([('type.id','=',4)]).ids
        consultant_fee_datas = self.env['consultant.fee'].search([('year','=',self.year)])
        for line in consultant_fee_datas:
            temp.append(line.normal_p_id.id)

        data_line = list(set(normal_p_consultants) - set(consultant_fee_datas))
        target = self.env['normal.p'].browse(data_line)
        for line in target:
            self.env['consultant.fee'].create({
                'year':self.year,
                'fee_payable':Annual_consultants_fee,
                'fee_code': 'F' + str(self.year) + line.new_coding,
                'normal_p_id': line.id,
                'cashier':line.cashier_name.id,
                'key_in_user': self.key_in_user.id
            })
        return True