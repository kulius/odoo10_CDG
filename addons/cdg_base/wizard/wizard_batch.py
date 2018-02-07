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

    def confirm_donate(self):
        order = self.env['donate.single']
        res = []
        res_line = []
        if self.bridge_money == 0 and self.road_money == 0 and self.coffin_money ==0 and self.poor_help_money and self.noassign_money == 0:
            raise ValidationError(u'各項捐款種類之捐款金額皆為 0 ，請至少填入一項捐款種類之捐款金額')
        if self.payment_method is not 1 and self.payment_method is not 2 and self.payment_method is not 3 and self.payment_method is not 4:
            raise ValidationError(u'支付方法至少選取一個')
        if self.work_id.name is False:
            raise ValidationError(u'必須選取收費員')
        for line in self.donate_line:
            res_line = []
            for row in line.donate_family1:
                if row.is_donate is True:
                    res_line.append([0, 0, {
                        'donate_member': row.id,
                        'bridge_money':self.bridge_money,
                        'road_money': self.road_money,
                        'coffin_money': self.coffin_money,
                        'poor_help_money': self.poor_help_money,
                        'noassign_money': self.noassign_money,
                    }])
            order.create({
                'bridge': self.bridge,
                'road': self.road,
                'coffin': self.coffin,
                'poor_help': self.poor_help,
                'noassign':self.noassign,
                'bridge_money': self.bridge_money,
                'road_money': self.road_money,
                'coffin_money': self.coffin_money,
                'poor_help_money': self.poor_help_money,
                'noassign_money':self.noassign_money,
                'donate_member': line.id,
                'family_check': res_line,
                'donate_date':self.donate_date,
                'work_id':self.work_id.id,
                'key_in_user':self.key_in_user.id,
                'payment_method':self.payment_method
            })
        action = self.env.ref('cdg_base.donate_single_view_action').read()[0] #
        return action

    @api.onchange('bridge', 'road', 'coffin', 'poor_help','noassign')
    def set_default_price(self):
        if self.bridge and self.bridge_money == 0:
            self.bridge_money = 100
        elif self.bridge is False:
            self.bridge_money = 0
        if self.road and self.road_money == 0:
            self.road_money = 100
        elif self.road is False:
            self.road_money = 0
        if self.coffin and self.coffin_money == 0:
            self.coffin_money = 100
        elif self.coffin is False:
            self.coffin_money = 0
        if self.poor_help and self.poor_help_money == 0:
            self.poor_help_money = 100
        elif self.poor_help is False:
            self.poor_help_money = 0
        if self.noassign and self.noassign_money == 0:
            self.noassign_money = 100
        elif self.noassign is False:
            self.noassign_money = 0


    @api.onchange('bridge_money', 'road_money', 'coffin_money', 'poor_help_money','noassign_money')
    def set_checkbox_check(self):
        if self.bridge_money != 0:
            self.bridge = True
        else:
            self.bridge = False
        if self.road_money != 0:
            self.road = True
        else:
            self.road = False
        if self.coffin_money != 0:
            self.coffin = True
        else:
            self.coffin = False
        if self.poor_help_money != 0:
            self.poor_help = True
        else:
            self.poor_help = False
        if self.noassign_money != 0:
            self.noassign = True
        else:
            self.noassign = False

