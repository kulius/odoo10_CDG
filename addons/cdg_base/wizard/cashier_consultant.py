# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class CashierConsultant(models.Model):
    _name = 'cashier.consultant'
    block_num = fields.Integer('格子數量')
    from_target = fields.Many2many(comodel_name='normal.p')

    def cashier_consultant_num(self):
        if (self.block_num > 12):
            raise ValidationError(u'格子數不能超越13格')

        data = {
            'block_num': self.block_num,
            'from_target': self.from_target.ids
        }
        return self.env['report'].get_action([], 'cdg_base.receipt_cashier_roll_consultant_template', data)