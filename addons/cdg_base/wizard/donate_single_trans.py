# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DonateSingleTrans(models.Model):
    _name = 'donate.single.trans'

    normal_p_code = fields.Many2one(comodel_name='normal.p',string='捐款者')
    donate_start_date = fields.Date('捐款時間-起')
    donate_end_date = fields.Date('捐款時間-訖')
    name = fields.Char('收件人')
    addr = fields.Char('收據地址')

    def donate_date_change(self):

        data = self.env['donate.single'].search([('donate_member', '=', self.normal_p_code.id), ('donate_date', '>=', self.donate_start_date), ('donate_date', '<=', self.donate_end_date)])

        for line in data:
            line.name = self.name
            line.rec_addr = self.addr

