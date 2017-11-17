# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class ReportDonateSingle(models.AbstractModel):
    _name = 'report.cdg_base.receipt_single_all_template'

    name = fields.Char()

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        target = self.env['donate.single'].browse(docids)

        date = datetime.datetime.strptime(target.create_date, "%Y-%m-%d %H:%M:%S")
        date = date.strftime("%Y-%m-%d")
        if target.state == 3:
            raise ValidationError(u'本捐款單已經作廢')
        elif target.state == 1:
            target.state = 2
        big = self.convert(target.donate_total)
        one = self.env['donate.order']
        two = self.env['donate.order']
        three = self.env['donate.order']
        if len(target.donate_list) > 10:

            for line in target.donate_list:
                if len(one) < 10:
                    one += line
                elif len(two) < 10:
                    two += line
                elif len(three) < 10:
                    three += line

        else:
            one = target.donate_list
        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.single',
            'docs': target.donate_list,
            'data': target,
            'big': big,
            'date': date,
            'one': one,
            'two': two,
            'three': three
        }
        return Report.render('cdg_base.receipt_single_all_template', docargs)

    def convert(self,n):
        units = ['', '萬', '億']
        nums = ['零', '壹', '贰', '參', '肆', '伍', '陸', '柒', '捌', '玖']
        decimal_label = ['角', '分']
        small_int_label = ['', '拾', '佰', '仟']
        int_part, decimal_part = str(int(n)), str(n - int(n))[2:]  # 分离整数和小数部分

        res = []
        if decimal_part:
            res.append(''.join([nums[int(x)] + y for x, y in zip(decimal_part, decimal_label) if x != '0']))

        if int_part != '0':
            while int_part:
                small_int_part, int_part = int_part[-4:], int_part[:-4]
                tmp = ''.join([nums[int(x)] + (y if x != '0' else '') for x, y in
                               zip(small_int_part[::-1], small_int_label)[::-1]])
                tmp = tmp.rstrip('零').replace('零零零', '零').replace('零零', '零')
                unit = units.pop(0)
                if tmp:
                    tmp += unit
                    res.append(tmp)
        return ''.join(res[::-1])


class ReportDonateSingleIndependent(models.AbstractModel):
    _name = 'report.cdg_base.receipt_single_independent_template'

    name = fields.Char()

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        target = self.env['donate.single'].browse(docids)

        if target.state == 3:
            raise ValidationError(u'本捐款單已經作廢')
        elif target.state == 1:
            target.state = 2
        boss = 0
        for line in target.donate_list:
            if line.donate_member.number == '1':
                boss = line.donate_member
                break
        res = self.env['donate.order']
        for line in target.donate_list:
            exist = False
            for list in res:
                if list.donate_member == line.donate_member:
                    exist = True
            if exist is False:
                res += line
        for list in res:
            price = 0
            for line in target.donate_list:
                if line.donate_member == list.donate_member:
                    price += line.donate

            list.report_price = price
            big = self.convert(price)
            list.report_big = big

        date = datetime.datetime.strptime(target.create_date, "%Y-%m-%d %H:%M:%S")
        date = date.strftime("%Y-%m-%d")

        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.batch',
            'docs': target.donate_list,
            'boss': res,
            'date': date,
            'data': target,
        }
        return Report.render('cdg_base.receipt_single_independent_template', docargs)

    def convert(self, n):
        units = ['', '萬', '億']
        nums = ['零', '壹', '贰', '參', '肆', '伍', '陸', '柒', '捌', '玖']
        decimal_label = ['角', '分']
        small_int_label = ['', '拾', '佰', '仟']
        int_part, decimal_part = str(int(n)), str(n - int(n))[2:]  # 分离整数和小数部分

        res = []
        if decimal_part:
            res.append(''.join([nums[int(x)] + y for x, y in zip(decimal_part, decimal_label) if x != '0']))

        if int_part != '0':
            while int_part:
                small_int_part, int_part = int_part[-4:], int_part[:-4]
                tmp = ''.join([nums[int(x)] + (y if x != '0' else '') for x, y in
                               zip(small_int_part[::-1], small_int_label)[::-1]])
                tmp = tmp.rstrip('零').replace('零零零', '零').replace('零零', '零')
                unit = units.pop(0)
                if tmp:
                    tmp += unit
                    res.append(tmp)
        return ''.join(res[::-1])