# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import ValidationError
import datetime


class HouseYearReport(models.AbstractModel):
    _name = 'report.cdg_base.house_year'

    # 計算該捐款款者在該年度共捐了多少錢
    def count_year_donate_total(self, one, year):
        count_total = 0
        for line in one.donate_history_ids:
            # 轉換時間字串 >> 時間物件
            lien_date = datetime.datetime.strptime(line.donate_date, '%Y-%m-%d')
            if lien_date.year == year:
                count_total += line.donate
        return count_total

    @api.multi
    def render_html(self, docids, data=None):
        active_ids = self.env.context.get('active_ids')
        house_hold = self.env['normal.p'].search([('id', 'in', active_ids)])
        report_year = data.get('report_year')
        key_in_user = data.get('key_in_user')
        house_total = 0
        order_doc = []
        if house_hold.id != house_hold.parent.id:
            house_hold = house_hold.parent
        if len(house_hold) != 1:
            raise ValidationError(u'錯誤!!，找不到該戶長，或傳入的戶長資料有兩筆以上')
        for line in house_hold.donate_family1:
            donate_price = self.count_year_donate_total(line, report_year)
            if donate_price != 0:
                house_total += donate_price
                order_temp = {
                    'name': line.name,
                }
                order_doc.append(order_temp)
        big_price = self.convert(house_total)
        docargs = {
            'house_hold': house_hold,
            'docs': house_total,
            'people':order_doc,
            'year': str(report_year) + u'年度收據',
            'report_year': str(report_year) + '-12-31',
            'print_user':key_in_user,
            'big_price':big_price
        }
        return self.env['report'].render('cdg_base.house_year', values=docargs)

    @api.depends('donate_line')
    def compute_price(self):
        for line in self:
            price = 0
            for row in line.donate_line:
                price += row.donate_price
            line.title_total_price = price
            line.title_total_price_big = self.convert(price)

    def convert(self, n):
        units = ['', '萬', '億']
        nums = ['零', '壹', '貳', '參', '肆', '伍', '陸', '柒', '捌', '玖']
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

class HouseYearSingleReport(models.AbstractModel):
    _name = 'report.cdg_base.house_year_personal'

    # 計算該捐款款者在該年度共捐了多少錢
    def count_year_donate_total(self, one, year):
        count_total = 0
        for line in one.donate_history_ids:
            # 轉換時間字串 >> 時間物件
            lien_date = datetime.datetime.strptime(line.donate_date, '%Y-%m-%d')
            if lien_date.year == year:
                count_total += line.donate
        return count_total

    @api.multi
    def render_html(self, docids, data=None):
        active_ids = self.env.context.get('active_ids')
        house_hold = self.env['normal.p'].search([('id', 'in', active_ids)])
        report_year = data.get('report_year')
        key_in_user = data.get('key_in_user')
        house_total = 0
        checking_point = False

        if house_hold.id != house_hold.parent.id:
            house_hold = house_hold.parent
        if len(house_hold) != 1:
            raise ValidationError(u'錯誤!!，找不到該戶長，或傳入的戶長資料有兩筆以上')
        order_doc = []
        for line in house_hold.donate_family1:
            house_total = self.count_year_donate_total(line, report_year)
            if house_total != 0:
                checking_point = True
                big_price = self.convert(house_total)
                order_temp = {
                    'ID':line.id,
                    'new_coding': line.new_coding,
                    'w_id':line.w_id,
                    'name': line.name,
                    'zip':line.zip,
                    'rec_addr': line.rec_addr,
                    'personal_total':house_total,
                    'big_price':big_price,
                    'year':str(report_year) + u'年度收據',
                    'report_year': str(report_year) + '-12-31',
                    'print_user':key_in_user,
                }
                order_doc.append(order_temp)
        if checking_point == False: # 此戶在該年度無任何捐款紀錄
            order_temp = {
                'ID': line.id,
                'new_coding': line.new_coding,
                'w_id': line.w_id,
                'name': line.name,
                'zip': line.zip,
                'rec_addr': line.rec_addr,
                'personal_total': 0,
                'big_price': u'%s年無捐款紀錄' % str(report_year),
                'year': str(report_year) + u'年度收據',
                'report_year': str(report_year) + '-12-31',
                'print_user': key_in_user,
            }
            order_doc.append(order_temp)
        docargs = {
            'docs': order_doc
        }
        return self.env['report'].render('cdg_base.house_year_personal', values=docargs)

    @api.depends('donate_line')
    def compute_price(self):
        for line in self:
            price = 0
            for row in line.donate_line:
                price += row.donate_price

            line.title_total_price = price
            line.title_total_price_big = self.convert(price)

    def convert(self, n):
        units = ['', '萬', '億']
        nums = ['零', '壹', '貳', '參', '肆', '伍', '陸', '柒', '捌', '玖']
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
