# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import ValidationError
import datetime

class ItemsReceiptPrint(models.AbstractModel):
    _name = 'report.cdg_base.items_receipt_print'

    @api.multi
    def render_html(self, docids, data=None):
        target = self.env['items.donate'].browse(data['ID'])
        print_date = ''
        tax_id_number = ''
        invoice_number = ''
        line_data = []
        for line in target:
            if line.print_state == True:
                print_date = u'補單日期: ' + datetime.date.today().strftime('%Y-%m-%d')
            elif line.print_state == False:
                print_date = ''
            # 金額大寫寫在這裡
            if line.tax_id_number:
                tax_id_number = u'統一編號: %s' % line.tax_id_number
            elif not line.tax_id_number:
                tax_id_number = ''
            if line.invoice_number:
                invoice_number = u'發票號碼: %s' % line.invoice_number
            elif not line.invoice_number:
                invoice_number = ''
            money = self.convert(line.money)
            line_data.append({
                'items_id': line.items_id,
                'donate_date': line.donate_date,
                'name': line.name,
                'addr': line.addr,
                'money': line.money,
                'big_money':money,
                'number': u'數量: %s' % line.number,
                'item_name': u'品名: %s' % line.item_name,
                'tax_id_number': tax_id_number,
                'invoice_number': invoice_number,
                'key_in_user': line.key_in_user.name,
                'print_state': print_date
            })
        docargs = {
            'docs': line_data,
        }
        for line in target:
            line.print_state = True
        return self.env['report'].render('cdg_base.items_donate_receipt', values=docargs)

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