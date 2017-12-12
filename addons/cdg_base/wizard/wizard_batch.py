# -*- coding: utf-8 -*-
from odoo import models, fields, api


class WizardDonate(models.Model):
    _name = 'wizard.batch'

    name = fields.Char()
    bridge = fields.Boolean(string='造橋')
    road = fields.Boolean(string='補路')
    coffin = fields.Boolean(string='施棺')
    poor_help = fields.Boolean(string='貧困扶助')
    others = fields.Boolean(string='不指名')
    bridge_money = fields.Integer(string='$')
    road_money = fields.Integer(string='$')
    coffin_money = fields.Integer(string='$')
    poor_help_money = fields.Integer(string='$')
    others_money = fields.Integer(string='$')
    donate_date = fields.Date('捐款日期',default=lambda self: fields.date.today())
    donate_line = fields.Many2many(comodel_name='normal.p', string='捐款批次的人')

    def confirm_donate(self):
        order = self.env['donate.single']
        res = []
        res_line = []
        for line in self.donate_line:
            res_line = []
            for row in line.donate_family1:
                if row.is_donate is True:
                    res_line.append([0, 0, {
                        'donate_member': row.id
                    }])
            order.create({
                'bridge': self.bridge,
                'road': self.road,
                'coffin': self.coffin,
                'poor_help': self.poor_help,
                'others':self.others,
                'bridge_money': self.bridge_money,
                'road_money': self.road_money,
                'coffin_money': self.coffin_money,
                'poor_help_money': self.poor_help_money,
                'others_money':self.others_money,
                'donate_member': line.id,
                'family_check': res_line,
                'donate_date':self.donate_date
            })
        action = self.env.ref('cdg_base.donate_single_view_action').read()[0] #
        return action

    @api.onchange('bridge', 'road', 'coffin', 'poor_help','others')
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
        if self.others and self.others_money == 0:
            self.others_money = 100

    @api.onchange('bridge_money', 'road_money', 'coffin_money', 'poor_help_money','others_money')
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
        if self.others_money != 0:
            self.others = True
        else:
            self.others = False
