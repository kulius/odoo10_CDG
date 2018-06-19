# -*- coding:utf-8
from odoo import api,fields,models

class CreditDebitMethod(models.Model):
    _name = "credit.debit.method"

    debit_method = fields.Selection(selection=[(1, '5日扣款'), (2, '20日扣款'), (3, '季日扣款'), (4, '年繳扣款'), (5, '單次扣款')],
                                    string='信用卡扣款方式')

    def set_debit_method(self):
        data = self.env['normal.p'].search([('debit_method','=',self.debit_method),('is_donated_credit','=',True)])
        for data in data:
            data.donate_batch_setting = True
        action = self.env.ref('cdg_base.credit_action').read()[0]
        action['context'] = {}  # remove default domain condition in search box
        action['domain'] = [('debit_method', '=', self.debit_method),('is_donated_credit','=',True)]  # set new domain condition to search data
        return action