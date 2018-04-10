# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WizardCashierDonor(models.Model):
    _name = 'wizard.abandon.single'

    donate_single_code = fields.Many2one(comodel_name='donate.single', string='捐款檔')

    def set_abandon(self):

        data = self.env['donate.single'].search([('donate_id','=',self.donate_single_code.donate_id)])

        for line in data:
            if line.state == 3:
                raise ValidationError(u'本捐款單已作廢!!')

            for line2 in line.donate_list:
                if line2.used_money != 0:
                    raise ValidationError(
                        u'本捐款單的 %s 先生/小姐 施棺捐款 %s 元整，已支出!! 因此無法作廢或退費，感謝您的善心' % (line2.donate_member.name, line2.donate))

            for line2 in line.donate_list:
                line2.state = 2
                line2.active = False


            line.state = 3
            line.active = False





