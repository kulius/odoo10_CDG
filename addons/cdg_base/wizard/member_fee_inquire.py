# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class memnberfeeinquire(models.Model):
    _name = 'memnber.fee.inquire'

    star_year = fields.Integer(string='繳費年度-起')
    end_year = fields.Integer(string='繳費年度-訖')
    member_type = fields.Selection(selection=[(1, '基本會員'), (2, '贊助會員')], string='會員種類')
    payment = fields.Selection(selection=[(1, '已繳費'), (2, '未繳費')], string='繳費狀況')

    def memnber_fee_search(self):

        if self.star_year == 0 or self.end_year == 0:
            raise ValidationError(u'請正確輸入繳費年度!')
        if self.star_year > self.end_year:
            raise ValidationError(u'[繳費年度-起] 不得大於 [繳費年度-訖]')
        number = 0
        action = self.env.ref('cdg_base.member_fee_only_view_action').read()[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        if self.payment is False and self.member_type is False:
            action['domain'] = [('year', '>=', self.star_year),('year', '<=', self.end_year),'|',('normal_p_id.type.id', '=', 2),('normal_p_id.type.id', '=', 3),('normal_p_id.booklist','=',True)]
            number = len(self.env['associatemember.fee'].search([('year', '>=', self.star_year),('year', '<=', self.end_year),'|',('normal_p_id.type.id', '=', 2),('normal_p_id.type.id', '=', 3),('normal_p_id.booklist','=',True)]))
        elif self.member_type == 1:
            if self.payment ==1:
                action['domain'] = [('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 2),('fee_date','!=',False),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 2),('fee_date','!=',False),('normal_p_id.booklist','=',True)]))
            elif self.payment ==2:
                action['domain'] = [('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 2),('fee_date','=',False),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 2),('fee_date','=',False),('normal_p_id.booklist','=',True)]))
            elif self.payment is False:
                action['domain'] = [('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 2),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 2),('normal_p_id.booklist','=',True)]))
        elif self.member_type == 2:
            if self.payment ==1:
                action['domain'] = [('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 3),('fee_date','!=',False),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 3),('fee_date','!=',False),('normal_p_id.booklist','=',True)]))
            elif self.payment ==2:
                action['domain'] = [('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 3),('fee_date','=',False),('normal_p_id.booklist','=',True),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 3),('fee_date','=',False),('normal_p_id.booklist','=',True)]))
            elif self.payment is False:
                action['domain'] = [('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 3),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', self.star_year),('year', '<=', self.end_year),('normal_p_id.type.id', '=', 3),('normal_p_id.booklist','=',True)]))
        action['views'] = [
            [self.env.ref('cdg_base.member_fee_search_tree').id, 'tree'],
            [self.env.ref('cdg_base.member_fee_only_view_form').id, 'form'],
        ]
        action['limit'] = number
        return action