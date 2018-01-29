# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class cashiersearchdonor(models.Model):
    _name = 'cashier.search.donor'

    year_start = fields.Char(string='繳費年度')
    year_end = fields.Char()
    name = fields.Char('捐款人姓名')
    payment = fields.Selection(selection=[(1, '已繳費'), (2, '未繳費')], string='繳費狀況')


    def cashier_donor_search(self):
        if (self.year_start and self.year_end is False) or (self.year_start is False and self.year_end):
            raise ValidationError(u'繳費年度任一欄不能為空白')
        number = 0
        if len(self.year) < 3:
            self.year = '0'+ str(self.year)
        action = self.env.ref('cdg_base.member_fee_only_view_action').read()[0]
        action2 = self.env.ref().read('cdg_base.')[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box

        if self.year_start is False and self.year_end is False and self.name is False and self.payment is False:
            action['domain'] = [('year', '=', self.year), '|', ('normal_p_id.type.id', '=', 2),('normal_p_id.type.id', '=', 3)]
            number = len(self.env['associatemember.fee'].search([('year', '=', self.year), '|', ('normal_p_id.type.id', '=', 2), ('normal_p_id.type.id', '=', 3)]))


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