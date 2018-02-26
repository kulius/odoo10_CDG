# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class CashierBlock(models.AbstractModel):
    _name = 'cashier.block'
    block_num = fields.Integer('格子數量')
    from_target = fields.Many2many(comodel_name='normal.p')

    def cashier_block_num(self):
        data = {
            'block_num': self.block_num,
            'from_target': self.from_target.ids
        }
        return self.env['report'].get_action([], 'cdg_base.receipt_cashier_roll_donor_template', data)
