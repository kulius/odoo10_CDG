# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class consultantfeeinquire(models.Model):
    _name = 'consultant.fee.inquire'
    _description = u'顧問費查詢'

    star_year = fields.Integer(string='繳費年度-起')
    end_year = fields.Integer(string='繳費年度-訖')
    payment = fields.Selection(selection=[(1, '已繳費'), (2, '未繳費')], string='繳費狀況')

    def consultant_fee_search(self):
        if self.star_year == 0 or self.end_year == 0:
            raise ValidationError(u'請正確輸入繳費年度!')
        if self.star_year > self.end_year:
            raise ValidationError(u'[繳費年度-起] 不得大於 [繳費年度-訖]')
        number = 0
        action = self.env.ref('cdg_base.consultant_fee_only_view_action').read()[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        if self.payment is False:
            action['domain'] = [('year', '>=', self.star_year),('year', '<=', self.end_year)]
            number = len(self.env['consultant.fee'].search([('year', '>=', self.star_year),('year', '<=', self.end_year)]))
        if self.payment == 1:
            action['domain'] = [('year', '>=', self.star_year),('year', '<=', self.end_year), ('normal_p_id.type.id', '=', 4), ('fee_date', '!=', False)]
            number = len(self.env['consultant.fee'].search([('year', '>=', self.star_year),('year', '<=', self.end_year), ('normal_p_id.type.id', '=', 4), ('fee_date', '!=', False)]))
        elif self.payment == 2:
            action['domain'] = [('year', '>=', self.star_year),('year', '<=', self.end_year), ('normal_p_id.type.id', '=', 4), ('fee_date', '=', False)]
            number = len(self.env['consultant.fee'].search([('year', '>=', self.star_year),('year', '<=', self.end_year), ('normal_p_id.type.id', '=', 4), ('fee_date', '=', False)]))
        action['views'] = [
            [self.env.ref('cdg_base.consultant_fee_search_tree').id, 'tree'],
            [self.env.ref('cdg_base.consultant_base_form').id, 'form'],
        ]
        action['limit'] = number
        return action