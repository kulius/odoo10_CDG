# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CashierTransfer(models.Model):

    _name = 'cashier.transfer'
    new_cashier = fields.Many2one(comodel_name='cashier.base', string="新收費員")
    from_target = fields.Many2many(comodel_name='normal.p')

    def cashier_transfer_to_other(self):
        for donor in self.from_target:
            donor.cashier_name = self.new_cashier
        return True