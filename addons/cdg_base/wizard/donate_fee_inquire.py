# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class donatefeeinquire(models.Model):
    _name = "donate.fee.inquire"

    year_start = fields.Char('繳費年度')
    year_end = fields.Char()

    #用時間來做查詢，先不顯示在畫面上

    name = fields.Char('捐款者')


    def donate_fee_search(self):

        if self.name is False:
            raise ValidationError(u'請輸入捐款者姓名!')
        number = 0
        action = self.env.ref('cdg_base.donate_order_action').read()[0]
        action['context'] = {}  # remove default domain condition in search box
        action['domain'] = []  # remove any value in search box

        action['domain'] = [('donate_member.name', '=', self.name)]
        number = len(self.env['donate.order'].search([('donate_member.name', '=', self.name)]))

        action['views'] = [
            [self.env.ref('cdg_base.donate_order_inquire_tree').id, 'tree'],
        ]

        action['limit'] = number

        return action