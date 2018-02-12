# -*- coding: utf-8 -*-
from odoo import models, fields, api

class memnberfeegenerate(models.Model):
    _name = 'memnber.fee.generate'
    _description = u'會員費產生'

    year = fields.Integer(string='繳費年度')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', default=lambda self: self.env.uid)

    def start_member_batch(self):
        basic_setting = self.env['ir.config_parameter'].search([])
        Annual_membership_fee = 0
        for line in basic_setting:
            if line.key == 'Annual_membership_fee':
                Annual_membership_fee = int(line.value)
        if self.year == 4:
            self.year = self.year - 1911

        sql = "SELECT DISTINCT on (member_id) * FROM normal_p WHERE member_id <>'' and con_addr<>'' "
        self._cr.execute(sql)
        dict = self._cr.dictfetchall()
        for i in range(len(dict)):
            self.env['associatemember.fee'].create({
                'year': self.year,
                'fee_payable': Annual_membership_fee,
                'normal_p_id': dict[i]['id'],
                'cashier': dict[i]['cashier_name'],
                'key_in_user': self.key_in_user.id
            })
        return True
