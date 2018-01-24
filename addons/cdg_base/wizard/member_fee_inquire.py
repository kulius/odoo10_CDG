# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class memnberfeeinquire(models.Model):
    _name = 'memnber.fee.inquire'

    year = fields.Char(string='繳費年度')
    member_type = fields.Selection(selection=[(1, '基本會員'), (2, '贊助會員')], string='會員種類')
    payment = fields.Selection(selection=[(1, '已繳費'), (2, '未繳費')], string='繳費狀況')

    def memnber_fee_search(self):
        if self.year is False:
            raise ValidationError(u'請輸入繳費年度!')
        number = 0
        action = self.env.ref('cdg_base.member_fee_only_view_action').read()[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        if self.payment is False and self.member_type is False:
            action['domain'] = [('year', '=', self.year),'|',('normal_p_id.type.id', '=', 2),('normal_p_id.type.id', '=', 3)]
            number = len(self.env['associatemember.fee'].search([('year', '=', self.year),'|',('normal_p_id.type.id', '=', 2),('normal_p_id.type.id', '=', 3)]))
        elif self.member_type == 1:
            if self.payment ==1:
                action['domain'] = [('year', '=', self.year),('normal_p_id.type.id', '=', 2),('fee_date','!=',False)]
                number = len(self.env['associatemember.fee'].search([('year', '=', self.year),('normal_p_id.type.id', '=', 2),('fee_date','!=',False)]))
            elif self.payment ==2:
                action['domain'] = [('year', '=', self.year),('normal_p_id.type.id', '=', 2),('fee_date','=',False)]
                number = len(self.env['associatemember.fee'].search([('year', '=', self.year),('normal_p_id.type.id', '=', 2),('fee_date','=',False)]))
            elif self.payment is False:
                action['domain'] = [('year', '=', self.year),('normal_p_id.type.id', '=', 2)]
                number = len(self.env['associatemember.fee'].search([('year', '=', self.year),('normal_p_id.type.id', '=', 2)]))
        elif self.member_type == 2:
            if self.payment ==1:
                action['domain'] = [('year', '=', self.year),('normal_p_id.type.id', '=', 3),('fee_date','!=',False)]
                number = len(self.env['associatemember.fee'].search([('year', '=', self.year),('normal_p_id.type.id', '=', 3),('fee_date','!=',False)]))
            elif self.payment ==2:
                action['domain'] = [('year', '=', self.year),('normal_p_id.type.id', '=', 3),('fee_date','=',False)]
                number = len(self.env['associatemember.fee'].search([('year', '=', self.year),('normal_p_id.type.id', '=', 3),('fee_date','=',False)]))
            elif self.payment is False:
                action['domain'] = [('year', '=', self.year),('normal_p_id.type.id', '=', 3)]
                number = len(self.env['associatemember.fee'].search([('year', '=', self.year),('normal_p_id.type.id', '=', 3)]))
        action['views'] = [
            [self.env.ref('cdg_base.member_fee_search_tree').id, 'tree'],
        ]

        action['limit'] = number

        return action