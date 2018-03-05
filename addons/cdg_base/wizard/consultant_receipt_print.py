# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class consultantreceiptprint(models.Model):
    _name = 'consultant.receipt'
    _description = u'顧問費收據列印'

    pay_year = fields.Integer(string='繳費年度')
    cdg_consultant = fields.Many2one(comodel_name='normal.p', string='顧問')
    print_user = fields.Many2one(comodel_name='res.users', string='列印人員', default=lambda self: self.env.uid)

    def consultant_receipt_print(self):
        datas = self.env['consultant.fee'].search([('normal_p_id','=',self.cdg_consultant.id),('year','=',self.pay_year)])
        if datas:
            if datas.fee_date == False:
                raise ValidationError(u'請輸入繳費日期')
            else:
                data = {
                    'consultant_id': datas.id,
                    'print_user': self.print_user.id,
                }
                return self.env['report'].get_action([], 'cdg_base.consultant_receipt_print', data)
        else:
            raise ValidationError(u'系統未找到資料')
        return True