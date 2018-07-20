# _*_ coding: utf-8 _*_
from odoo import models, api,fields
from odoo.exceptions import ValidationError
import datetime

class DonateSingleReport(models.Model):
    _name = 'donate.single.report'
    _description = u'報表用來整理收據資料用table'

    title_donate = fields.Many2one(comodel_name='normal.p', string='收據收件人')
    donate_wizard = fields.Many2one(comodel_name='wizard.batch',string='捐款日期')
    title_doante_code = fields.Char(string='捐款編號')
    title_doante_date = fields.Char(string='捐款日期')
    title_work_id = fields.Char(string='收費員')
    title_Make_up_date=fields.Char(string='日期',default=lambda self: fields.date.today())
    title_state = fields.Integer(string='列印狀態')
    donate_line = fields.One2many(comodel_name='report.line',inverse_name='parent_id', string='個人捐款明細')
    title_total_price = fields.Integer(string='捐款總金額', compute='compute_price', store=True)
    title_total_price_big = fields.Char(string='金額大寫', compute='compute_price', store=True)
    title_year_fee = fields.Integer(string='年繳')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', states={2: [('readonly', True)]})
    work_id = fields.Many2one(comodel_name='cashier.base', string='收費員', states={2: [('readonly', True)]})

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

class ReportLine(models.Model):
    _name = 'report.line'

    parent_id = fields.Many2one(comodel_name='donate.single.report')
    donate_id = fields.Char(string='捐款編號')
    donate_member_id = fields.Many2one(comodel_name='normal.p', string='收據收件人')
    name = fields.Char(string='捐款姓名')
    donate_type = fields.Selection(selection=[(01, '造橋'), (02, '補路'), (03, '施棺'), (05, '貧困扶助'), (06, '一般捐款')],
                                   string='捐款種類')
    donate_price = fields.Integer(string='捐款金額')
    is_merge = fields.Boolean(string='是否合併收據')
    print_all_donor_list = fields.Boolean(string='列印願意捐助的眷屬')

class ReportDonateSingleMerge(models.AbstractModel):
    _name = 'report.cdg_base.donate_single_merge'

    @api.multi
    def render_html(self, docids, data=None):
        docs = self.env['donate.single'].browse(docids)
        for line in docs:
            line.report_donate = line.donate_date
            if line.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif line.state == 1:
                # line.state = 2
                line.print_count+=1
                line.print_date = datetime.date.today()
                line.print_user = self.env.uid
            elif line.state == 2:
                line.print_date = datetime.date.today()

        res_doc= []
        for line in docs.sorted(key=lambda r: r.donate_id):
            order_doc = []
            for order_line in line.donate_list:
                order_temp = {
                    'donate_id':order_line.donate_id,
                    'donate_member':order_line.donate_member.name,
                    'donate_type':dict(order_line.fields_get(allfields=['donate_type'])['donate_type']['selection'])[order_line.donate_type],
                    'donate':order_line.donate,
                }
                order_doc.append(order_temp)
            line.report_price_big = self.convert(line.donate_total)
            donor_code = ''
            if line.donate_member.w_id == False:
                donor_code = line.donate_member.new_coding
            else:
                donor_code = "%s (%s)" % (line.donate_member.new_coding, line.donate_member.w_id)
            temp = {
                'donate_id': line.donate_id,
                'donate_member': line.donate_member.name,
                'zip':line.donate_member.zip,
                'rec_addr': line.donate_member.rec_addr,
                'new_coding': donor_code,
                'donate_date': line.donate_date,
                'donate_total': line.donate_total,
                'key_in_user': line.key_in_user.name,
                'work_id': line.work_id.c_id + line.work_id.name,
                'report_price_big': line.report_price_big,
                'print_date': line.print_date,
                'state': line.state,
                'year_fee': line.year_fee,
                'rec_send':line.donate_member.rec_send,
                'order_line':order_doc
            }
            res_doc.append(temp)

        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.single',
            'docs': res_doc,
        }
        for row in docs:
            if row.state == 1:
                row.state = 2
        return self.env['report'].render('cdg_base.donate_single_merge', values=docargs)

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

#---------------------以下為測試報表--------------------------------

# class ReceiptTest(models.AbstractModel):
#     _name = 'report.cdg_base.receipt_test'
# 
#     @api.model
#     def render_html(self, docids, data=None):
#         target = self.env['donate.single'].browse(docids)
#         res = self.env['donate.order']
#         res_line = self.env['donate.order']
#         report_line = self.env['donate.single.report']
#         for row in target:
#             if row.state == 3:
#                 raise ValidationError(u'本捐款單已經作廢')
            


class ReportDonateSinglePersonal(models.AbstractModel):
    _name = 'report.cdg_base.donate_single_personal'

    @api.multi
    def render_html(self, docids, data=None):
        target = self.env['donate.single'].browse(docids)
        res = self.env['donate.order']
        res_line = self.env['donate.order']
        report_line = self.env['donate.single.report']
        for row in target.sorted(key=lambda r: r.donate_id):
            if row.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif row.state == 1:
                # row.state = 2
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
        for line in res.sorted(key=lambda r: r.donate_id):
            single_state = 0
            if line.donate_list_id.year_fee:
                single_state = 1
            elif not line.donate_list_id.year_fee:
                single_state = 2
            tmp_id = report_line.create({
                'title_donate': line.donate_member.id,
                'title_doante_code': line.donate_id,
                'title_doante_date':line.donate_date,
                'key_in_user':line.key_in_user.id,
                'work_id': line.cashier.id,
                'title_Make_up_date': datetime.date.today(),
                'title_state':line.donate_list_id.state,
                'title_year_fee': single_state
            })

            line_data = []
            for row in res_line:
                if row.donate_member == line.donate_member and row.donate_id == line.donate_id:
                    line_data.append([0, 0, {
                        'donate_id':row.donate_id,
                        'donate_member_id':line.donate_member.id,
                        'name': row.donate_member.name,
                        'donate_type': row.donate_type,
                        'donate_price': row.donate,
                    }])

            tmp_id.write({
                'donate_line': line_data
            })
            report_line += tmp_id

        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.single',
            'docs': report_line,
        }
        for row in target:
            if row.state == 1:
                row.state = 2
        return self.env['report'].render('cdg_base.donate_single_personal', values=docargs)

class ReportDonateSingleOneKindOnePerson(models.AbstractModel):
    _name = 'report.cdg_base.donate_single_one_kind_one_person'

    @api.multi
    def render_html(self,docids, data=None):
        target = self.env['donate.single'].browse(docids)
        res = self.env['donate.order']
        report_line = self.env['donate.single.report']

        for row in target:
            if row.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif row.state == 1:
                # row.state = 2
                row.print_count += 1
                row.print_date=datetime.date.today()
                row.print_user = self.env.uid

            for line in row.donate_list:
                res += line
        for line in res:
            single_state = 0
            if line.donate_list_id.year_fee:
                single_state = 1
            elif not line.donate_list_id.year_fee:
                single_state = 2
            tmp_id = report_line.create({
                'title_donate': line.donate_member.id,
                'title_doante_code': line.donate_id,
                'title_doante_date': line.donate_date,
                'key_in_user': line.key_in_user.id,
                'work_id': line.cashier.id,
                'title_state': line.donate_list_id.state,
                'title_year_fee': single_state
            })

            line_data = []
            line_data.append([0, 0, {
                'name': line.donate_member.name,
                'donate_type': line.donate_type,
                'donate_price': line.donate
            }])
            for lines in target:
                tmp_id.write({'title_work_id': lines.work_id.name,'title_Make_up_date': datetime.date.today()})

            tmp_id.write({
                'donate_line': line_data
            })
            report_line += tmp_id

        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.single',
            'docs': report_line,
        }
        for row in target:
            if row.state == 1:
                row.state = 2
        return self.env['report'].render('cdg_base.donate_single_one_kind_one_person', values=docargs)



class ReportDonateSingleDefault(models.AbstractModel):
    _name = 'report.cdg_base.donate_single_default'

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        target = self.env['donate.single'].browse(docids)
        report_line = self.env['donate.single.report']

        for row in target.sorted(key=lambda r: r.donate_id):
            res = self.env['donate.order']
            merge_res_line = self.env['donate.order']
            res_line = self.env['donate.order']
            if row.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif row.state == 1:
                # row.state = 2
                row.print_count += 1
                row.print_date = datetime.date.today()
                row.print_user = self.env.uid

            # 檢查捐款列表
            for line in row.donate_list:
                if line.donate_member.is_merge is True:
                    merge_res_line += line
                else:
                    res_line += line
                    exist = False
                    for list_one in res:
                        if list_one.donate_member == line.donate_member and list_one.donate_id == line.donate_id:
                            exist = True
                    if exist is False:
                        res += line
            # 直接針對donate_single的資料進行整理
            single_state = 0
            if row.year_fee:
                single_state = 1
            elif not row.year_fee:
                single_state = 2
            # 判定是否有人需要印合併收據。
            if len(merge_res_line) !=0:
                tmp_id = report_line.create({
                    'title_donate': row.donate_member.id,
                    'title_doante_code': row.donate_id,
                    'key_in_user': line.key_in_user.id,
                    'work_id': row.work_id.id,
                    'title_doante_date': row.donate_date,
                    'title_work_id': row.work_id.name,
                    'title_Make_up_date': datetime.date.today(),
                    'title_state': row.state,
                    'title_year_fee': single_state
                })
                line_data = []
                for line in merge_res_line:
                    line_data.append([0, 0, {
                        'donate_id': line.donate_id,
                        'name': line.donate_member.name,
                        'donate_member_id': line.donate_member.id,
                        'donate_type': line.donate_type,
                        'donate_price': line.donate,
                        'is_merge': line.donate_member.is_merge
                    }])
                tmp_id.write({
                    'donate_line': line_data
                })
                report_line += tmp_id

            # 找出不合併列印的人，整理後放進報表用table

            for line in res:
                single_state = 0
                if line.donate_list_id.year_fee:
                    single_state = 1
                elif not line.donate_list_id.year_fee:
                    single_state = 2
                not_merge_tmp_id = report_line.create({
                    'title_donate': line.donate_member.id,
                    'title_doante_code': line.donate_id,
                    'key_in_user': line.key_in_user.id,
                    'work_id': line.cashier.id,
                    'title_doante_date': line.donate_date,
                    'title_work_id': line.cashier.name,
                    'title_Make_up_date': datetime.date.today(),
                    'title_state': row.state,
                    'title_year_fee': single_state
                })
                line_data = []
                for row_one in res_line:
                    if line.donate_member == row_one.donate_member:
                        line_data.append([0, 0, {
                            'donate_id': row_one.donate_id,
                            'name': row_one.donate_member.name,
                            'donate_member_id': row_one.donate_member.id,
                            'donate_type': row_one.donate_type,
                            'donate_price': row_one.donate,
                            'is_merge': row_one.donate_member.is_merge,
                    }])
                not_merge_tmp_id.write({
                    'donate_line': line_data
                })
                report_line += not_merge_tmp_id
        docargs = {
            'doc_ids': docids,
            'doc_model': 'donate.single',
            'docs': report_line,
        }
        for row in target:
            if row.state == 1:
                row.state = 2
        return self.env['report'].render('cdg_base.donate_single_default', values=docargs)

class ReportMemberReceiptPrint(models.AbstractModel):
    _name = 'report.cdg_base.member_receipt_print'

    @api.model
    def render_html(self, docids, data=None):
        target = self.env['associatemember.fee'].browse(data['member_id'])
        print_again = data.get('print_again')
        if print_again == True:
            print_date = u'補單日期: ' + datetime.date.today().strftime('%Y-%m-%d')
        elif print_again == False:
            print_date = ''

        line_data = []
        for line in target:
            # 金額大寫寫在這裡
            money = self.convert(line.fee_payable)
            donor_code = ''
            if line.normal_p_id.member_id == False:
                donor_code = line.normal_p_id.new_coding
            else:
                donor_code = "%s (%s)" % (line.normal_p_id.new_coding, line.normal_p_id.member_id)
            line_data.append({
                'member_name': line.member_name,
                'pay_date': line.fee_date,
                'fee_code':line.fee_code,
                'year':line.year,
                'fee_payable':line.fee_payable,
                'cashier': line.cashier.name,
                'zip': line.zip,
                'rec_addr':line.rec_addr,
                'new_coding': donor_code,
                'key_in_user': line.key_in_user.name,
                'fee_payable':line.fee_payable,
                'price_big': money,
                'cashier':line.cashier.c_id + line.cashier.name,
                'type': u'常年會費',
                'print_date':print_date,
            })

        docargs = {
            'docs': line_data,
        }
        return self.env['report'].render('cdg_base.member_fee_print', values=docargs)

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

class ReportConsultantReceiptPrint(models.AbstractModel):
    _name = 'report.cdg_base.consultant_receipt_print'

    @api.model
    def render_html(self, docids, data=None):
        target = self.env['consultant.fee'].browse(data['consultant_id'])
        print_again = data.get('print_again')
        if print_again == True:
            print_date = u'補單日期: ' + datetime.date.today().strftime('%Y-%m-%d')
        elif print_again == False:
            print_date = ''

        line_data = []
        for line in target:
            # 金額大寫寫在這裡
            money = self.convert(line.fee_payable)
            donor_code = ''
            if line.normal_p_id.consultant_id == False:
                donor_code = line.normal_p_id.new_coding
            else:
                donor_code = "%s (%s)" % (line.normal_p_id.new_coding, line.normal_p_id.consultant_id)
            line_data.append({
                'member_name': line.consultant_name,
                'pay_date': line.fee_date,
                'fee_code':line.fee_code,
                'year':line.year,
                'fee_payable':line.fee_payable,
                'cashier': line.cashier.name,
                'zip':line.zip,
                'rec_addr':line.rec_addr,
                'new_coding': donor_code,
                'key_in_user': line.key_in_user.name,
                'fee_payable':line.fee_payable,
                'price_big': money,
                'cashier':line.cashier.c_id + line.cashier.name,
                'type': u'顧問費',
                'print_date': print_date,
            })

        docargs = {
            'docs': line_data,
        }
        return self.env['report'].render('cdg_base.member_fee_print', values=docargs)

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

# --------------------------------------- 舊案收據列印--------------------------------------

class DonateSingleReport(models.Model):
    _name = 'old.donate.single.report'
    _description = u'報表用來整理收據資料用table'

    title_donate = fields.Many2one(comodel_name='normal.p', string='收據收件人')
    donate_wizard = fields.Many2one(comodel_name='wizard.batch',string='捐款日期')
    title_doante_code = fields.Char(string='捐款編號')
    title_doante_date = fields.Char(string='捐款日期')
    title_work_id = fields.Char(string='收費員')
    title_Make_up_date=fields.Char(string='日期',default=lambda self: fields.date.today())
    title_state = fields.Integer(string='列印狀態')
    donate_line = fields.One2many(comodel_name='old.report.line',inverse_name='parent_id', string='個人捐款明細')
    title_total_price = fields.Integer(string='捐款總金額', compute='compute_price', store=True)
    title_total_price_big = fields.Char(string='金額大寫', compute='compute_price', store=True)
    title_year_fee = fields.Integer(string='年繳')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', states={2: [('readonly', True)]},default=lambda self: self.env.uid)
    work_id = fields.Many2one(comodel_name='cashier.base', string='收費員', states={2: [('readonly', True)]})

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

class ReportLine(models.Model):
    _name = 'old.report.line'

    parent_id = fields.Many2one(comodel_name='old.donate.single.report')
    donate_id = fields.Char(string='捐款編號')
    donate_member_id = fields.Many2one(comodel_name='normal.p', string='收據收件人')
    name = fields.Char(string='捐款姓名')
    donate_type = fields.Selection(selection=[(01, '造橋'), (02, '補路'), (03, '施棺'), (05, '貧困扶助'), (06, '一般捐款')],
                                   string='捐款種類')
    donate_price = fields.Integer(string='捐款金額')
    is_merge = fields.Boolean(string='是否合併收據')
    print_all_donor_list = fields.Boolean(string='列印願意捐助的眷屬')

class ReportDonateSingleMerge(models.AbstractModel):
    _name = 'report.cdg_base.old_donate_single_merge'

    @api.multi
    def render_html(self, docids, data=None):
        docs = self.env['old.donate.single'].browse(docids)
        for line in docs:
            line.report_donate = line.donate_date
            if line.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif line.state == 1:
                # line.state = 2
                line.print_count+=1
                line.print_date = datetime.date.today()
                line.print_user = self.env.uid
            elif line.state == 2:
                line.print_date = datetime.date.today()

        res_doc= []
        for line in docs:
            order_doc = []
            for order_line in line.donate_list:
                order_temp = {
                    'donate_id':order_line.donate_id,
                    'donate_member':order_line.donate_member.name,
                    'donate_type':dict(order_line.fields_get(allfields=['donate_type'])['donate_type']['selection'])[order_line.donate_type],
                    'donate':order_line.donate,
                }
                order_doc.append(order_temp)
            line.report_price_big = self.convert(line.donate_total)
            temp = {
                'donate_id': line.donate_id,
                'donate_member': line.donate_member.name,
                'rec_addr': line.rec_addr,
                'new_coding': line.donate_member.new_coding,
                'donate_date': line.donate_date,
                'donate_total': line.donate_total,
                'key_in_user': line.key_in_user.name,
                'work_id': line.work_id.name,
                'report_price_big': line.report_price_big,
                'print_date': line.print_date,
                'state': line.state,
                'year_fee': line.year_fee,
                'rec_send':line.donate_member.rec_send,
                'order_line':order_doc
            }
            res_doc.append(temp)

        docargs = {
            'doc_ids': docids,
            'doc_model': 'old.donate.single',
            'docs': res_doc,
        }
        for row in docs:
            if row.state == 1:
                row.state = 2
        return self.env['report'].render('cdg_base.donate_single_merge', values=docargs)

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

class ReportDonateSinglePersonal(models.AbstractModel):
    _name = 'report.cdg_base.old_donate_single_personal'

    @api.multi
    def render_html(self, docids, data=None):
        target = self.env['old.donate.single'].browse(docids)
        res = self.env['old.donate.order']
        res_line = self.env['old.donate.order']
        report_line = self.env['old.donate.single.report']
        for row in target:
            if row.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif row.state == 1:
                # row.state = 2
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
            single_state = 0
            if line.donate_list_id.year_fee:
                single_state = 1
            elif not line.donate_list_id.year_fee:
                single_state = 2
            tmp_id = report_line.create({
                'title_donate': line.donate_member.id,
                'title_doante_code': line.donate_id,
                'title_doante_date':line.donate_date,
                'work_id': line.cashier.id,
                'title_Make_up_date': datetime.date.today(),
                'title_state':line.donate_list_id.state,
                'title_year_fee': single_state
            })

            line_data = []
            for row in res_line:
                if row.donate_member == line.donate_member and row.donate_id == line.donate_id:
                    line_data.append([0, 0, {
                        'donate_id':row.donate_id,
                        'donate_member_id':line.donate_member.id,
                        'name': row.donate_member.name,
                        'donate_type': row.donate_type,
                        'donate_price': row.donate,
                    }])

            tmp_id.write({
                'donate_line': line_data
            })
            report_line += tmp_id

        docargs = {
            'doc_ids': docids,
            'doc_model': 'old.donate.single',
            'docs': report_line,
        }
        for row in target:
            if row.state == 1:
                row.state = 2
        return self.env['report'].render('cdg_base.donate_single_personal', values=docargs)

class ReportDonateSingleOneKindOnePerson(models.AbstractModel):
    _name = 'report.cdg_base.old_donate_single_one_kind_one_person'

    @api.multi
    def render_html(self,docids, data=None):
        target = self.env['old.donate.single'].browse(docids)
        res = self.env['old.donate.order']
        report_line = self.env['old.donate.single.report']

        for row in target:
            if row.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif row.state == 1:
                # row.state = 2
                row.print_count += 1
                row.print_date=datetime.date.today()
                row.print_user = self.env.uid

            for line in row.donate_list:
                res += line
        for line in res:
            single_state = 0
            if line.donate_list_id.year_fee:
                single_state = 1
            elif not line.donate_list_id.year_fee:
                single_state = 2
            tmp_id = report_line.create({
                'title_donate': line.donate_member.id,
                'title_doante_code': line.donate_id,
                'work_id': line.cashier.id,
                'title_state': line.donate_list_id.state,
                'title_year_fee': single_state
            })

            line_data = []
            line_data.append([0, 0, {
                'name': line.donate_member.name,
                'donate_type': line.donate_type,
                'donate_price': line.donate
            }])
            for line in target:
                tmp_id.write({'title_doante_date': line.donate_date,'title_work_id': line.work_id.name,'title_Make_up_date': datetime.date.today()})

            tmp_id.write({
                'donate_line': line_data
            })
            report_line += tmp_id

        docargs = {
            'doc_ids': docids,
            'doc_model': 'old.donate.single',
            'docs': report_line,
        }
        for row in target:
            if row.state == 1:
                row.state = 2
        return self.env['report'].render('cdg_base.donate_single_one_kind_one_person', values=docargs)

class ReportDonateSingleDefault(models.AbstractModel):
    _name = 'report.cdg_base.old_donate_single_default'

    @api.model
    def render_html(self, docids, data=None):
        target = self.env['old.donate.single'].browse(docids)
        report_line = self.env['old.donate.single.report']

        for row in target:
            res = self.env['old.donate.order']
            merge_res_line = self.env['old.donate.order']
            res_line = self.env['old.donate.order']
            if row.state == 3:
                raise ValidationError(u'本捐款單已經作廢')
            elif row.state == 1:
                # row.state = 2
                row.print_count += 1
                row.print_date = datetime.date.today()
                row.print_user = self.env.uid

            # 檢查捐款列表
            for line in row.donate_list:
                if line.donate_member.is_merge is True:
                    merge_res_line += line
                else:
                    res_line += line
                    exist = False
                    for list_one in res:
                        if list_one.donate_member == line.donate_member and list_one.donate_id == line.donate_id:
                            exist = True
                    if exist is False:
                        res += line
            # 直接針對donate_single的資料進行整理
            single_state = 0
            if line.donate_list_id.year_fee:
                single_state = 1
            elif not line.donate_list_id.year_fee:
                single_state = 2
            # 判定是否有人需要印合併收據。
            if len(merge_res_line) !=0:
                tmp_id = report_line.create({
                    'title_donate': row.donate_member.id,
                    'title_doante_code': row.donate_id,
                    'work_id': row.work_id.id,
                    'title_doante_date': row.donate_date,
                    'title_work_id': row.work_id.name,
                    'title_Make_up_date': datetime.date.today(),
                    'title_state': row.state,
                    'title_year_fee': single_state
                })
                line_data = []
                for line in merge_res_line:
                    line_data.append([0, 0, {
                        'donate_id': line.donate_id,
                        'name': line.donate_member.name,
                        'donate_member_id': line.donate_member.id,
                        'donate_type': line.donate_type,
                        'donate_price': line.donate,
                        'is_merge': line.donate_member.is_merge
                    }])
                tmp_id.write({
                    'donate_line': line_data
                })
                report_line += tmp_id

            # 找出不合併列印的人，整理後放進報表用table

            for line in res:
                single_state = 0
                if line.donate_list_id.year_fee:
                    single_state = 1
                elif not line.donate_list_id.year_fee:
                    single_state = 2
                not_merge_tmp_id = report_line.create({
                    'title_donate': line.donate_member.id,
                    'title_doante_code': line.donate_id,
                    'work_id': line.cashier.id,
                    'title_doante_date': line.donate_date,
                    'title_work_id': line.cashier.name,
                    'title_Make_up_date': datetime.date.today(),
                    'title_state': line.state,
                    'title_year_fee': single_state
                })
                line_data = []
                for row_one in res_line:
                    if line.donate_member == row_one.donate_member:
                        line_data.append([0, 0, {
                            'donate_id': row_one.donate_id,
                            'name': row_one.donate_member.name,
                            'donate_member_id': row_one.donate_member.id,
                            'donate_type': row_one.donate_type,
                            'donate_price': row_one.donate,
                            'is_merge': row_one.donate_member.is_merge,
                    }])
                not_merge_tmp_id.write({
                    'donate_line': line_data
                })
                report_line += not_merge_tmp_id
        docargs = {
            'doc_ids': docids,
            'doc_model': 'old.donate.single',
            'docs': report_line,
        }
        for row in target:
            if row.state == 1:
                row.state = 2
        return self.env['report'].render('cdg_base.donate_single_default', values=docargs)