# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WizardCashierDonor(models.Model):
    _name = 'wizard.donate.time'
    cashier_code = fields.Many2one(comodel_name='cashier.base',string='收費員')
    donate_id_start = fields.Char('收據編號-起')
    donate_id_end = fields.Char('收據編號-訖')
    key_in_user_code = fields.Many2one(comodel_name='res.users',string="建檔人員",domain=['|',('login', 'like', 'A00') ,('login', 'like', 'A50')])
    donate_date = fields.Date('捐款日期')

    def donate_time(self):

        data = self.env['donate.single'].search([('key_in_user','=',self.key_in_user_code.id),('donate_id','>=',self.donate_id_start),('donate_id','<=',self.donate_id_end),('work_id','=',self.cashier_code.id),('state','=',1)])

        for line in data:
            line.donate_date = self.donate_date
            for line2 in line.donate_list:
                line2.donate_date = self.donate_date




