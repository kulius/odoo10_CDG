# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class consultantfeeinquire(models.Model):
    _name = 'coffin.inquire'

    year_start = fields.Date(string='繳費期間')
    year_end = fields.Date()

    def coffin_search(self):
        # if(self.year_start and self.year_end is False) or (self.year_start is not False and self.year_end):
        #     raise ValidationError(u'繳費期間任一格欄位請勿空白!')

        number = 0
        action = self.env.ref('cdg_base.coffin_base_action').read()[0]
        action['context'] = {}  # remove default domain condition in search box
        action['domain'] = []  # remove any value in search box

        # if not self.year_start and not self.year_end and not self.dealer:
        if  self.year_end  and  self.year_start:
            action['domain'] = [('coffin_date', '>=', self.year_start),('coffin_date', '<=', self.year_end)]
            number = len(self.env['coffin.base'].search([('coffin_date', '>=', self.year_start),('coffin_date', '<=', self.year_end)]))


        action['limit'] = number

        action['views'] = [
            [self.env.ref('cdg_base.coffin_base_tree').id, 'tree'],
        ]





        return action