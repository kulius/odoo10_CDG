# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import *

class consultantreceiptprint(models.Model):
    _name = 'consultant.receipt'
    _description = u'顧問費收據列印'

    pay_year = fields.Integer(string='繳費年度', default=datetime.today().year - 1911)
    cdg_consultant = fields.Many2one(comodel_name='normal.p', string='顧問')
    print_user = fields.Many2one(comodel_name='res.users', string='列印人員', default=lambda self: self.env.uid)
    print_again = fields.Boolean(string='補單')

    def consultant_receipt_print(self):
        active_ids = self.env.context.get('active_ids')
        datas = self.env['consultant.fee'].search([('normal_p_id','=',active_ids),('year','=',self.pay_year)])
        if datas:
            if datas.fee_date == False:
                raise ValidationError(u'請輸入繳費日期')
            else:
                data = {
                    'consultant_id': datas.id,
                    'print_user': self.print_user.id,
                    'print_again':self.print_again
                }
                return self.env['report'].get_action([], 'cdg_base.consultant_receipt_print', data)
        else:
            raise ValidationError(u'系統未找到資料')
        return True