# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CashierTransfer(models.TransientModel):
    _name = 'cashier.transfer'

    old_cashier = fields.Many2one(comodel_name='cashier.base', string="原收費員")
    new_cashier = fields.Many2one(comodel_name='cashier.base', string="新收費員")
    from_target = fields.Many2many(comodel_name='normal.p', string="捐款者名單")

    def cashier_transfer_to_other(self):
        if self.old_cashier == self.new_cashier:
            raise ValidationError(u'原收費員是%s, 新收費員是%s, 請重新確認要合併的收費員' % (self.old_cashier.name, self.new_cashier.name))
        for line in self.from_target:
           line.cashier_name = self.new_cashier