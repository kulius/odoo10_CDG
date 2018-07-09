# -*- coding:utf-8
from odoo import api,fields,models

class CreditDebitMethod(models.Model):
    _name = "credit.debit.method"

    debit_method = fields.Selection(selection=[(1, '5日扣款'), (2, '20日扣款'), (3, '季日扣款'), (4, '年繳扣款'), (5, '單次扣款')],
                                    string='信用卡扣款方式')

    def set_debit_method(self):
        data = self.env['normal.p'].search([('debit_method','=',self.debit_method),('credit_family','!=',False)])
        number = 0
        for line in data:
            line.donate_batch_setting = True
            number = number + 1
        action = self.env.ref('cdg_base.credit_action').read()[0]
        action['context'] = {}  # remove default domain condition in search box
        action['limit'] = number
        action['domain'] = [('debit_method', '=', self.debit_method),('credit_family','!=',False)]  # set new domain condition to search data
        return action