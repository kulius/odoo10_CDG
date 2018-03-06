# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WizardDonate(models.Model):
    _name = 'wizard.batch'

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
    donate_date = fields.Date('捐款日期',default=lambda self: fields.date.today())
    payment_method = fields.Selection([(1, '現金'), (2, '郵政劃撥'), (3, '信用卡扣款'), (4, '銀行轉帳'), (5, '支票')], string='繳費方式')
    donate_line = fields.Many2many(comodel_name='normal.p', string='捐款批次的人')
    work_id = fields.Many2one(comodel_name='cashier.base', string='收費員')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', states={2: [('readonly', True)]},default=lambda self: self.env.uid)
    sum_donor_num = fields.Integer(string='捐款人數',compute = 'compute_donate_data')
    sum_donate_total = fields.Integer(string='捐款總額',compute = 'compute_donate_data')
    clean_all_check = fields.Boolean(string='清除所有 [確認] 按鈕')

    def compute_donate_data(self):
        self.sum_donor_num = 0
        self.sum_donate_total = 0
        for line in self.donate_line:
            if line.donate_batch_setting:
                for row in line.donate_family1:
                    if row.is_donate is True:
                        self.sum_donor_num += 1
                        self.sum_donate_total += row.last_donate_money
        return True

    def confirm_donate(self):
        order = self.env['donate.single']
        res = []
        res_line = []
        if self.payment_method is not 1 and self.payment_method is not 2 and self.payment_method is not 3 and self.payment_method is not 4:
            raise ValidationError(u'支付方法至少選取一個')
        if self.work_id.name is False:
            raise ValidationError(u'必須選取收費員')
        for line in self.donate_line:
            res_line = []
            if line.donate_batch_setting:
                for row in line.donate_family1:
                    if line.new_coding == row.new_coding and (row.is_donate is False or row.last_donate_type is False or row.last_donate_money == 0):
                        raise ValidationError(u'捐款者編號 : %s，因戶長並無捐款意願，而無法透過 [收費員批次捐款] 捐款，請至 [捐款作業] 進行捐款，謝謝。 ' % line.new_coding)
                    if row.is_donate is True:
                        row.last_donate_date = self.donate_date
                        if row.last_donate_type == 1:
                            self.bridge_money = row.last_donate_money
                            self.bridge = True
                        elif row.last_donate_type == 2:
                            self.road_money = row.last_donate_money
                            self.road = True
                        elif row.last_donate_type == 3:
                            self.coffin_money = row.last_donate_money
                            self.coffin = True
                        elif row.last_donate_type == 5:
                            self.poor_help_money = row.last_donate_money
                            self.poor_help = True
                        elif row.last_donate_type == 6:
                            self.noassign_money = row.last_donate_money
                            self.noassign = True
                        else:
                            self.bridge_money = 0
                            self.road_money = 0
                            self.coffin_money = 0
                            self.poor_help_money = 0
                            self.noassign_money = 0

                        res_line.append([0, 0, {
                            'donate_member': row.id,
                            'bridge_money':self.bridge_money,
                            'road_money': self.road_money,
                            'coffin_money': self.coffin_money,
                            'poor_help_money': self.poor_help_money,
                            'noassign_money': self.noassign_money,
                        }])
                        self.bridge_money = 0
                        self.road_money = 0
                        self.coffin_money = 0
                        self.poor_help_money = 0
                        self.noassign_money = 0
                order.create({
                    'donate_member': line.id,
                    'family_check': res_line,
                    'donate_date':self.donate_date,
                    'work_id':self.work_id.id,
                    'key_in_user':self.key_in_user.id,
                    'payment_method':self.payment_method,
                })
            if self.clean_all_check:
                line.donate_batch_setting = False
        action = self.env.ref('cdg_base.donate_single_view_action').read()[0] #
        return action