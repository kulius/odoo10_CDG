# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ChangDonater(models.Model):
    _name = 'chang.donater'

    new_target = fields.Many2one(comodel_name='normal.p', string='目標捐款人')
    from_target = fields.Many2one(comodel_name='normal.p', string='原始捐款人')

    def active_to_transfer(self):
        # 更新眷屬
        if self.from_target.donate_family1.ids:
            for line in self.from_target.donate_family1:
                line.parent = self.new_target.id

        # 更新歷史紀錄
        if self.from_target.donate_history_ids.ids:
            for line in self.from_target.donate_history_ids:
                line.donate_member = self.new_target.id

        self.from_target.active = False



