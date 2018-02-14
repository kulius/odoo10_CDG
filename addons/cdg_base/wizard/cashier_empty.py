# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CashierEmpty(models.Model):
    _name = 'cashier.empty'

    num = fields.Integer('勾簽格子數量')

    def empty_block(self):
        data = {
            'num': self.num,
        }

        return self.env['report'].get_action([], 'cdg_base.receipt_empty_template',data)