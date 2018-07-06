# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WizardCreditBatch(models.Model):
    _name = 'wizard.credit.batch'

    name = fields.Char()
    bridge = fields.Boolean(string='造橋')
    road = fields.Boolean(string='補路')
    coffin = fields.Boolean(string='施棺')
    poor_help = fields.Boolean(string='貧困扶助')
    noassign = fields.Boolean(string='不指名')
    bridge_money = fields.Integer(string='$')
    road_money = fields.Integer(string='$')
    coffin_money = fields.Integer(string='$')
    poor_help_money = fields.Integer(string='$')
    noassign_money = fields.Integer(string='$')
    donate_date = fields.Date('捐款日期', default=lambda self: fields.date.today())
    payment_method = fields.Selection([(1, '現金'), (2, '郵政劃撥'), (3, '信用卡扣款'), (4, '銀行轉帳'), (5, '支票')], string='繳費方式', default=3)
    donate_line = fields.Many2many(comodel_name='normal.p', string='信用卡捐款批次的人')
    work_id = fields.Many2one(comodel_name='cashier.base', string='收費員' ,default = 371)
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', states={2: [('readonly', True)]},
                                  default=lambda self: self.env.uid)
    sum_donor_num = fields.Integer(string='捐款人數',compute='compute_credit_total_money')
    sum_donate_total = fields.Integer(string='捐款總額',compute='compute_credit_total_money')
    clean_all_check = fields.Boolean(string='清除所有 [確認] 按鈕', default=True)


    def compute_credit_total_money(self):
        self.sum_donor_num = 0
        self.sum_donate_total = 0
        for line in self.donate_line:
            if line.donate_batch_setting:
                for data in line.credit_parent.credit_family:
                    if data.is_donate == True:
                        self.sum_donor_num += 1
                    self.sum_donate_total += data.credit_total_money


    def confirm_donate(self):
        order = self.env['donate.single']

        if self.payment_method != 3:
            raise ValidationError(u'支付方法請選擇信用卡扣款')
        elif self.work_id.name is False:
            raise ValidationError(u'必須選取收費員')

        for data in self.donate_line:
            res_line = []
            if data.donate_batch_setting:
                for row in data.credit_parent.credit_family:
                    res_line.append([0, 0, {
                        'donate_member': row.id,
                        'bridge_money': row.credit_bridge_money,
                        'road_money': row.credit_road_money,
                        'coffin_money': row.credit_coffin_money,
                        'poor_help_money': row.credit_poor_money,
                        'noassign_money': row.credit_normal_money,
                        'donate_total': row.credit_bridge_money + row.credit_road_money + row.credit_coffin_money + row.credit_poor_money + row.credit_normal_money,
                    }])

                for line in data.credit_parent:
                        order.create({
                            'donate_member': line.credit_family[0].id,
                            'name': line.credit_family[0].name,
                            'debit_method':line.credit_family[0].debit_method,
                            'zip': data.credit_zip,
                            'rec_addr': data.credit_addr,
                            'zip_code': data.credit_zip,
                            'con_addr': data.credit_addr,
                            'con_phone': data.con_phone,
                            'cellphone': data.con_phone,
                            'family_check': res_line,
                            'donate_date': self.donate_date,
                            'work_id': self.work_id.id,
                            'key_in_user': self.key_in_user.id,
                            'payment_method': self.payment_method,
                            'receipt_send': data.is_sent,
                            'report_send': data.year_sent,
                        })

                if self.clean_all_check:
                    data.donate_batch_setting = False

        action = self.env.ref('cdg_base.donate_single_view_action').read()[0]
        action['domain'] = [('debit_method','!=', False),('state','=',1),('receipt_send','=',True)]
        return action