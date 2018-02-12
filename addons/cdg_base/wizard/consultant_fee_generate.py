# -*- coding: utf-8 -*-
from odoo import models, fields, api

class consultantfeegenerate(models.Model):
    _name = 'consultant.fee.generate'
    _description = u'顧問費產生'

    year = fields.Integer(string='繳費年度')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員',default=lambda self: self.env.uid)

    def start_consultant_batch(self):
        basic_setting = self.env['ir.config_parameter'].search([])
        Annual_consultants_fee = 0
        for line in basic_setting:
            if line.key == 'Annual_consultants_fee':
                Annual_consultants_fee = int(line.value)
        if self.year == 4:
            self.year = self.year - 1911

        sql = "SELECT DISTINCT on (consultant_id) * FROM normal_p WHERE consultant_id <>'' and con_addr<>'' "
        self._cr.execute(sql)
        dict = self._cr.dictfetchall()
        for i in range(len(dict)):
            self.env['consultant.fee'].create({
                'year':self.year,
                'fee_payable':Annual_consultants_fee,
                'normal_p_id': dict[i]['id'],
                'cashier':dict[i]['cashier_name'],
                'key_in_user':self.key_in_user.id
            })
        return True