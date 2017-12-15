# -*- coding: utf-8 -*-
from odoo import models, fields, api

class printcheck(models.Model):
    _name = 'print.check'

    flag = fields.Boolean(default=False)
    from_target = fields.Many2many(comodel_name='donate.single')

    def active_to_print(self):
        data = {
            'flag':self.flag,
            'from_target':self.from_target.ids
        }
        return self.env['report'].get_action([], 'cdg_base.receipt_single_default', data)