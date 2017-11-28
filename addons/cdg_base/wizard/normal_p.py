# -*- coding: utf-8 -*-
from odoo import models, fields, api


class WizardNormalP(models.Model):
    _name = 'normal.p.wizard'

    bridge = fields.Boolean(string='造橋')
    road = fields.Boolean(string='補路')
    coffin = fields.Boolean(string='施棺')
    poor_help = fields.Boolean(string='貧困扶助')
    bridge_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    road_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    coffin_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    poor_help_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    name = fields.Char(string='名稱')
    donate_line = fields.Many2many(comodel_name='normal.p', string='捐款批次的人')






    def confirm(self):
        for line in self.name:
            print line.id
        return True

    @api.onchange('bridge', 'road', 'coffin', 'poor_help')
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

    @api.onchange('bridge_money', 'road_money', 'coffin_money', 'poor_help_money')
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

