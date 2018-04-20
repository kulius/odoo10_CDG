# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CashierTransfer(models.Model):

    _name = 'cashier.transfer'

    out_cashier = fields.Many2one(comodel_name='cashier.base',string="移出收費員")
    current_cashier = fields.Many2one(comodel_name='cashier.base', string="當前收費員")

    def cashier_transfer_to_other(self):
        data = self.env['normal.p'].search([('cashier_name','=',self.out_cashier.id)])
        for line in data:
            line.cashier_name = self.current_cashier.id

        return self.env.ref('cdg_base.cashier_base_action').read()[0]

