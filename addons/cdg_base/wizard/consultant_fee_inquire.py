# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class consultantfeeinquire(models.Model):
    _name = 'consultant.fee.inquire'

    year = fields.Char(string='繳費年度')
    payment = fields.Selection(selection=[(1, '已繳費'), (2, '未繳費')], string='繳費狀況')

    def consultant_fee_search(self):
        if self.year is False:
            raise ValidationError(u'請輸入繳費年度!')
        number = 0
        action = self.env.ref('cdg_base.consultant_fee_only_view_action').read()[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        if self.payment is False:
            action['domain'] = [('year', '=', self.year)]
            number = len(self.env['consultant.fee'].search([('year', '=', self.year)]))
        if self.payment == 1:
            action['domain'] = [('year', '=', self.year), ('normal_p_id.type.id', '=', 4), ('fee_date', '!=', False)]
            number = len(self.env['consultant.fee'].search([('year', '=', self.year), ('normal_p_id.type.id', '=', 4), ('fee_date', '!=', False)]))
        elif self.payment == 2:
            action['domain'] = [('year', '=', self.year), ('normal_p_id.type.id', '=', 4), ('fee_date', '=', False)]
            number = len(self.env['consultant.fee'].search([('year', '=', self.year), ('normal_p_id.type.id', '=', 4), ('fee_date', '=', False)]))

        action['views'] = [
            [self.env.ref('cdg_base.consultant_fee_search_tree').id, 'tree'],
        ]

        action['limit'] = number

        return action