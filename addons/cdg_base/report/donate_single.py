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

        for line in target:
            line.report_donate = line.donate_date
            if line.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif line.state == 1:
                line.state = 2
                line.print_count+=1
                line.print_date = datetime.date.today()
                line.print_user = self.env.uid

            line.report_price_big = self.convert(line.donate_total)

        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.single',
            'docs': target,
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

class DonateSingleReport(models.Model):
    _name = 'donate.single.report'
    _description = u'報表用來整理收據資料用table'

    title_donate = fields.Many2one(comodel_name='normal.p', string='收據收件人')
    donate_wizard = fields.Many2one(comodel_name='wizard.batch',string='捐款日期')
    title_doante_code = fields.Char(string='捐款編號')
    title_doante_date = fields.Char(string='捐款日期')
    title_Make_up_date=fields.Char(string='日期',default=lambda self: fields.date.today())
    donate_line = fields.One2many(comodel_name='report.line',inverse_name='parent_id', string='個人捐款明細')
    title_total_price = fields.Integer(string='捐款總金額', compute='compute_price', store=True)
    title_total_price_big = fields.Char(string='金額大寫', compute='compute_price', store=True)

    @api.depends('donate_line')
    def compute_price(self):
        for line in self:
            price=0
            for row in line.donate_line:
                price += row.donate_price

            line.title_total_price = price
            line.title_total_price_big = self.convert(price)

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



class ReportLine(models.Model):
    _name = 'report.line'

    parent_id = fields.Many2one(comodel_name='donate.single.report')
    name = fields.Char(string='捐款姓名')
    donate_type = fields.Selection(selection=[(1, '造橋'), (2, '補路'), (3, '施棺'), (4, '貧困扶助'), (5, '其他工程')],
                                   string='捐款種類')
    donate_price = fields.Integer(string='捐款金額')




class ReportDonateSingleIndependent(models.AbstractModel):
    _name = 'report.cdg_base.receipt_single_independent_template'

    name = fields.Char()

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        target = self.env['donate.single'].browse(docids)
        res = self.env['donate.order']
        res_line = self.env['donate.order']
        report_line = self.env['donate.single.report']
        for row in target:
            if row.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif row.state == 1:
                row.state = 2
                row.print_count += 1
                row.print_date = datetime.date.today()
                row.print_user = self.env.uid

            for line in row.donate_list:
                res_line += line
                exist = False
                for list in res:
                    if list.donate_member == line.donate_member and list.donate_id == line.donate_id:
                        exist = True
                if exist is False:
                    res += line
        for line in res:
         #   date = datetime.datetime.strptime(line.create_date, "%Y-%m-%d %H:%M:%S")
         #   date_sring = date.strftime("%Y-%m-%d")
            tmp_id = report_line.create({
                'title_donate': line.donate_member.id,
                'title_doante_code': line.donate_id,
            })
            for line in target:
                tmp_id.write({'title_doante_date': line.donate_date})

            report_line += tmp_id
            line_data = []
            for row in res_line:
                if row.donate_member == line.donate_member and row.donate_id == line.donate_id:
                    line_data.append([0,0,{
                        'name': row.donate_member.name,
                        'donate_type' : row.donate_type,
                        'donate_price' : row.donate
                    }])
            tmp_id.write({
                'donate_line': line_data
            })
            report_line += tmp_id


        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.batch',
            'docs': report_line,

        }
        return Report.render('cdg_base.receipt_single_independent_template', docargs)


class ReportDonateSingleOneKindOnePerson(models.AbstractModel):
    _name = 'report.cdg_base.receipt_single_one_kind_one_person'

    @api.multi
    def render_html(self,docids, data=None):
        Report = self.env['report']
        target = self.env['donate.single'].browse(docids)
        res = self.env['donate.order']

        report_line = self.env['donate.single.report']
        for row in target:
            if row.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif row.state == 1:
                row.state = 2
                row.print_count += 1
                row.print_date=datetime.date.today()
                row.print_user = self.env.uid

            for line in row.donate_list:
                res += line
        for line in res:

            tmp_id = report_line.create({
                'title_donate': line.donate_member.id,
                'title_doante_code': line.donate_id,
            })

            line_data = []
            line_data.append([0, 0, {
                'name': line.donate_member.name,
                'donate_type': line.donate_type,
                'donate_price': line.donate
            }])
            for line in target:
                tmp_id.write({'title_doante_date': line.donate_date})

            tmp_id.write({
                'donate_line': line_data
            })
            report_line += tmp_id

        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.batch',
            'docs': report_line,

        }
        return Report.render('cdg_base.receipt_single_one_kind_one_person', docargs)


class ReportDonateSingleDefault(models.AbstractModel):
    _name = 'report.cdg_base.receipt_single_default'

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        target = self.env['donate.single'].browse(docids)
        res = self.env['donate.order']
        merge_res= self.env['donate.order']
        merge_res_line = self.env['donate.order']
        res_line = self.env['donate.order']
        report_line = self.env['donate.single.report']
        flag = False
        check_print =False

        if data:
            target = self.env['donate.single'].browse(data['from_target'])
            flag = data['flag']

        for row in target:
            if row.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif row.state == 1:
                row.state = 2
                row.print_count += 1
                row.print_date = datetime.date.today()
                row.print_user = self.env.uid
            elif flag == False and row.state == 2:
                check_print = True


            for line in row.donate_list:
                if line.donate_member == row.donate_member:
                    merge_exist = False
                    for list in merge_res:
                        if list.donate_member == line.donate_member and list.donate_id == line.donate_id:
                            merge_exist = True
                    if merge_exist is False:
                        merge_res += line

                if line.donate_member.is_merge is True:
                    merge_res_line += line
                else:
                    res_line += line
                    exist = False
                    for list in res:
                        if list.donate_member == line.donate_member and list.donate_id == line.donate_id:
                            exist = True
                    if exist is False:
                        res += line

        #if check_print  == True:
            #raise UserError(_(u'本捐款單已經作廢'))
        # 找出要合併列印的人，整理後放入報表用table

        for line in merge_res:

            tmp_id = report_line.create({
                'title_donate': line.donate_member.id,
                'title_doante_code': line.donate_id,
            })
            for line in target:
                tmp_id.write({'title_doante_date': line.donate_date})
            line_data = []
            for row in merge_res_line:
                if row.donate_id == line.donate_id:
                    line_data.append([0, 0, {
                        'name': row.donate_member.name,
                        'donate_type': row.donate_type,
                        'donate_price': row.donate
                    }])
            tmp_id.write({
                'donate_line': line_data
            })
            report_line += tmp_id

        # 找出不合併列印的人，整理後放進報表用table
        for line in res:
            date = datetime.datetime.strptime(line.create_date, "%Y-%m-%d %H:%M:%S")
            date_sring = date.strftime("%Y-%m-%d")
            tmp_id = report_line.create({
                'title_donate': line.donate_member.id,
                'title_doante_code': line.donate_id,
            })
            for line in target:
                tmp_id.write({'title_doante_date': line.donate_date})
            line_data = []
            for row in res_line:
                if row.donate_member == line.donate_member and row.donate_id == line.donate_id:
                    line_data.append([0, 0, {
                        'name': row.donate_member.name,
                        'donate_type': row.donate_type,
                        'donate_price': row.donate
                    }])
            tmp_id.write({
                'donate_line': line_data
            })
            report_line += tmp_id

        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.batch',
            'docs': report_line,
            'flag':flag
        }
        return Report.render('cdg_base.receipt_single_default', docargs)



