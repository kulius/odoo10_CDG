# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WizardCashierDonor(models.TransientModel):
    _name = 'wizard.abandon.single'

    donate_single_code = fields.Many2one(comodel_name='donate.single', string='捐款檔')

    def set_abandon(self):
        data = self.env['donate.single'].search([('id','=',self.donate_single_code.id)])

        for line in data:
            if line.state == 3:
                raise ValidationError(u'本捐款單已作廢!!')
            for row in line.donate_list:
                if row.used_money != 0:
                    raise ValidationError(u'本捐款單的 %s 先生/小姐 施棺捐款 %s 元整，已支出!! 因此無法作廢或退費，感謝您的善心' % (row.donate_member.name, row.donate))
                row.state = 2
                row.active = False
            line.state = 3
            line.active = False