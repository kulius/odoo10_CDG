# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import collections

class memnberfeeinquire(models.Model):
    _name = 'memnber.fee.inquire'
    _description = u'會員費查詢'

    star_year = fields.Char(string='繳費年度-起')
    end_year = fields.Char(string='繳費年度-訖')
    member_type = fields.Selection(selection=[(1, '基本會員'), (2, '贊助會員')], string='會員種類')
    payment = fields.Selection(selection=[(1, '已繳費'), (2, '未繳費')], string='繳費狀況')


    def memnber_fee_search(self):
        star_time = int(self.star_year)
        end_time = int(self.end_year)
        if self.star_year is False or self.end_year is False:
            raise ValidationError(u'請正確輸入繳費年度!')
        if star_time > end_time:
            raise ValidationError(u'[繳費年度-起] 不得大於 [繳費年度-訖]')
        number = 0
        action = self.env.ref('cdg_base.member_fee_only_view_action').read()[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        if self.payment is False and self.member_type is False:
            action['domain'] = [('year', '>=', star_time),('year', '<=', end_time),'|',('normal_p_id.type.id', '=', 2),('normal_p_id.type.id', '=', 3),('normal_p_id.booklist','=',True)]
            number = len(self.env['associatemember.fee'].search([('year', '>=', star_time),('year', '<=', end_time),'|',('normal_p_id.type.id', '=', 2),('normal_p_id.type.id', '=', 3),('normal_p_id.booklist','=',True)]))
        elif self.member_type == 1:
            if self.payment ==1:
                action['domain'] = [('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 2),('fee_date','!=',False),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 2),('fee_date','!=',False),('normal_p_id.booklist','=',True)]))
            elif self.payment ==2:
                action['domain'] = [('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 2),('fee_date','=',False),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 2),('fee_date','=',False),('normal_p_id.booklist','=',True)]))
            elif self.payment is False:
                action['domain'] = [('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 2),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 2),('normal_p_id.booklist','=',True)]))
        elif self.member_type == 2:
            if self.payment ==1:
                action['domain'] = [('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 3),('fee_date','!=',False),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 3),('fee_date','!=',False),('normal_p_id.booklist','=',True)]))
            elif self.payment ==2:
                action['domain'] = [('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 3),('fee_date','=',False),('normal_p_id.booklist','=',True),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 3),('fee_date','=',False),('normal_p_id.booklist','=',True)]))
            elif self.payment is False:
                action['domain'] = [('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 3),('normal_p_id.booklist','=',True)]
                number = len(self.env['associatemember.fee'].search([('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 3),('normal_p_id.booklist','=',True)]))
        action['views'] = [
            [self.env.ref('cdg_base.member_fee_search_tree').id, 'tree'],
        ]
        action['limit'] = number
        return action

    def print_excel(self):
        star_time = int(self.star_year)
        end_time = int(self.end_year)
        data_id = []
        temp_list = []
        number = end_time - star_time + 1

        if self.star_year is False or self.end_year is False:
            raise ValidationError(u'請正確輸入繳費年度!')
        if star_time > end_time:
            raise ValidationError(u'[繳費年度-起] 不得大於 [繳費年度-訖]')
        if self.payment is False or self.member_type is False:
           raise ValidationError(u'請設定會員種類以及繳費狀況')

        if self.member_type == 1:
            if self.payment == 1:
                data = self.env['associatemember.fee'].search([('year', '>=', star_time),('year', '<=', end_time),('normal_p_id.type.id', '=', 2),('fee_date','!=',False),('normal_p_id.booklist','=',True)],order='normal_p_id asc')
                data.sorted(key=lambda r: r.normal_p_id)
                s = collections.Counter()
                for line in data:
                    s[line.normal_p_id.id] += 1
                    if s[line.normal_p_id.id] == number:
                        data_id.append(line.id)
                docargs = {
                    'docs': data_id,
                }
                s.clear()
                return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'cdg_base.member_list.xlsx',
                    'datas': docargs
                }
            elif self.payment == 2:
                data = self.env['associatemember.fee'].search([('year', '>=', star_time), ('year', '<=', end_time), ('normal_p_id.type.id', '=', 2), ('fee_date', '=', False),('normal_p_id.booklist','=',True)], order='normal_p_id asc')
                for line in data:
                    if line.normal_p_id.id in temp_list:
                        continue
                    else:
                       data_id.append(line.id)
                    temp_list.append(line.normal_p_id.id)
                docargs = {
                    'docs': data_id,
                }
                return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'cdg_base.member_list.xlsx',
                    'datas': docargs
                }
        elif self.member_type == 2:
            if self.payment == 1:
                data = self.env['associatemember.fee'].search([('year', '>=', star_time), ('year', '<=', end_time), ('normal_p_id.type.id', '=', 3),('fee_date', '!=', False),('normal_p_id.booklist','=',True)], order='normal_p_id asc')
                s = collections.Counter()
                for line in data:
                    s[line.normal_p_id.id] += 1
                    if s[line.normal_p_id.id] == number:
                        data_id.append(line.id)
                docargs = {
                    'docs': data_id,
                }
                s.clear()
                return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'cdg_base.member_list.xlsx',
                    'datas': docargs
                }
            elif self.payment == 2:
                data = self.env['associatemember.fee'].search([('year', '>=', star_time), ('year', '<=', end_time), ('normal_p_id.type.id', '=', 3),('fee_date', '=', False),('normal_p_id.booklist','=',True)], order='normal_p_id asc')
                for line in data:
                    if line.normal_p_id.id in temp_list:
                        continue
                    else:
                       data_id.append(line.id)
                    temp_list.append(line.normal_p_id.id)
                docargs = {
                    'docs': data_id,
                }
                return {
                    'type': 'ir.actions.report.xml',
                    'report_name': 'cdg_base.member_list.xlsx',
                    'datas': docargs
                }




        # return True