# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class WizardCashierDonor(models.TransientModel):
    _name = 'wizard.cashier.donor'
    block_num = fields.Integer('格子數量')
    cashier_code = fields.Many2one(comodel_name='cashier.base',string='收費員')
    donate_start_date = fields.Date('捐款日期-起')
    donate_end_date = fields.Date('捐款日期-訖')
    from_target = fields.Many2many(comodel_name='normal.p')

    def cashier_block_num(self):
        if (self.block_num > 12):
            raise ValidationError(u'格子數不能超越13格')

        donate_data = self.env['normal.p'].search([('cashier_name','=',self.cashier_code.ids),('last_donate_date','>=',self.donate_start_date),('last_donate_date','<=',self.donate_end_date)]).ids

        data = {
            'block_num': self.block_num,
            'from_target': donate_data
        }
        return self.env['report'].get_action([], 'cdg_base.receipt_cashier_roll_donor_template', data)