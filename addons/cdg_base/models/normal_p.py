# -*- coding: utf-8 -*-
import time ,datetime
import psycopg2

from odoo import models, fields, api

# 一般人基本檔 團員 會員 收費員 顧問
import logging

_logger = logging.getLogger(__name__)


class NormalP(models.Model):
    # 捐款人
    _name = 'normal.p'
    _order = 'sequence,id'

    new_coding = fields.Char(string='新編捐款者編號')
    special_tag = fields.Boolean(string='眷屬檔沒有的團員')
    w_id = fields.Char(string='舊團員編號')
    number = fields.Char(string='序號')
    name = fields.Char(string='姓名')
    birth = fields.Date(string='生日')
    cellphone = fields.Char(string='手機')
    con_phone = fields.Char(string='連絡電話(一)')
    con_phone2 = fields.Char(string='連絡電話(二)')
    zip_code = fields.Char(string='郵遞區號')
    zip = fields.Char()
    key_in_user = fields.Many2one(comodel_name='c.worker', string='輸入人員', ondelete='cascade')
    db_chang_date = fields.Date(string='異動日期')
    build_date = fields.Date(string='建檔日期')


    email = fields.Char(string='Email')
    type = fields.Many2many(comodel_name='people.type', string='人員種類')
    self_iden = fields.Char(string='身分證字號')

    rec_addr = fields.Char(string='收據地址')
    con_addr = fields.Char(string='聯絡地址')
    send_addr = fields.Char(string='寄送地址')
    address = fields.Char(string='通訊地址')
    sex = fields.Selection(selection=[(1, '男生'), (2, '女生')], string='性別')
    come_date = fields.Date(string='到職日期')
    lev_date = fields.Date(string='離職日期')
    ps = fields.Text(string='備註')
    habbit_donate = fields.Selection(selection=[(01, '造橋'), (02, '補路'), (03, '施棺'), (04, '伙食費'), (05, '貧困扶助'),(06, '不指定'), (99, '其他工程')],
                                     string='喜好捐款')
    cashier_name = fields.Many2one(comodel_name='c.worker', string='收費員姓名', domain="[('job_type', '=', '2'), ]", ondelete='cascade')
    donate_cycle = fields.Selection(selection=[('03', '季繳'), ('06', '半年繳'), ('12', '年繳')], string='捐助週期')
    rec_type = fields.Selection(selection=[(1, '正常'), (2, '年收據')], string='收據狀態')
    rec_send = fields.Boolean(string='收據寄送')

    self = fields.Char(string='自訂排序')
    report_send = fields.Boolean(string='報表寄送')
    thanks_send = fields.Boolean(string='感謝狀寄送')
    prints = fields.Boolean(string='是否列印')
    prints_id = fields.Char(string='核印批號')
    prints_date = fields.Char(string='核印日期')
    bank_id = fields.Char(string='扣款銀行代碼')
    bank = fields.Char(string='扣款銀行')
    bank_id2 = fields.Char(string='扣款分行代碼')
    bank2 = fields.Char(string='扣款分行')
    account = fields.Char(string='扣款帳號')
    bank_check = fields.Boolean(string='銀行核印')
    ps2 = fields.Text(string='備註')

    comp_id = fields.Char(string='電腦編號')
    member_list = fields.Char(string='會員名冊編號')
    year = fields.Char(string='繳費年度')
    should_pay = fields.Integer(string='應繳金額')
    cashier = fields.Many2one(comodel_name='c.worker', string='收費員')
    pay_date = fields.Date(string='收費日期')
    booklist = fields.Boolean(string='名冊列印')
    member_type = fields.Selection(selection=[(1, '基本會員'), (2, '贊助會員')], string='會員種類')
    hire_date = fields.Date(string='雇用日期')
    merge_report = fields.Boolean(string='年收據合併', help='將捐款者的收據整合進該住址')


    # 來判斷你是不是老大
    parent = fields.Many2one(comodel_name='normal.p', string='戶長', ondelete='cascade')
    donate_family1 = fields.One2many(comodel_name='normal.p', inverse_name='parent', string='團員眷屬')
    member_data_ids = fields.Many2one(comodel_name='member.data', string='關聯的顧問會員檔')
    donate_history_ids = fields.One2many(comodel_name='donate.order', inverse_name='donate_member')



    member_pay_history = fields.One2many(comodel_name='associatemember.fee', inverse_name='normal_p_id')
    consultant_pay_history = fields.One2many(comodel_name='consultant.fee', inverse_name='normal_p_id')

    sequence = fields.Integer(string='排序')
    is_donate = fields.Boolean(string='是否捐助', default=True)
    is_merge = fields.Boolean(string='是否合併收據', default=True)

    donate_family_list = fields.Char(string='眷屬列表', compute='compute_faamily_list')
    active = fields.Boolean(default=True)

    def action_chang_donater_wizard(self):

        wizard_data = self.env['chang.donater'].create({
            'from_target': self.id
        })

        action = self.env.ref('cdg_base.chang_donater_action').read()[0]
        action['res_id'] = wizard_data.id
        return action

    def historypersonal(self):
        action = self.env.ref('cdg_base.donate_single_view_action').read()[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        action['domain'] = ['&',('donate_member', '=', self.new_coding),('state','!=',3)] # set new domain condition to search data
        return action

    def donate_batch(self,ids):
        res = []
        for line in ids:
            res.append([4, line])
        wizard_data = self.env['wizard.batch'].create({
            'donate_line': res

        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.batch',
            'name': '批次捐款項目',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }


    @api.depends('donate_family1.is_donate','donate_family1.is_merge')
    def compute_faamily_list(self):
        for line in self:
            sb = ''
            str = ''
            for row in line.donate_family1:
                if row.is_donate is False:
                    str += u'(X)' + row.name + ','
                elif row.is_merge is False:
                    sb += u'(★)'+ row.name + ','
                else:
                    sb += row.name + ','
            line.donate_family_list = sb+str

    def toggle_donate(self):
        self.is_donate = not self.is_donate

    def toggle_merge(self):
        self.is_merge = not self.is_merge


    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), '|', ('w_id', operator, name), '|', ('new_coding', operator, name),
                      '|', ('self_iden',operator, name), ('con_addr', operator, name)]

        banks = self.search(domain + args, limit=limit)
        return banks.name_get()

    @api.multi
    def my_self(self):
        return [('parent', '=', self.id)]


    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "{%s} %s" % (record.new_coding, record.name)
            result.append((record.id, name))
        return result

    def input_member(self):
        max_id = 753395
        member_data = self.env['member.data'].search([])
        new_id = ""
        i = 1
        type_id = 0
        for line in member_data:
            _logger.error(' %s / %s', i, len(member_data))
            if line.conn_zip_code != "":
                new_id = line.conn_zip_code[:3] + str(max_id)
            else:
                new_id = '000' + str(max_id)

            self.create({
                'new_coding': new_id,
                'name': line.name,
                'self_iden': line.user_id,
                'birth': line.birthday,
                'cellphone': line.cellphone,
                'con_phone': line.phone1,
                'con_phone2': line.phone2,
                'zip_code': line.conn_zip_code,
                'con_addr': line.conn_address,
                'member_data_ids': line.id,
                'type': self.check_type(line)
            })
            i = i + 1
            max_id = max_id + 1

    def check_type(self, line):
        if line.member_type.id > 0:
            return [(4, line.member_type.id)]
        else:
            return None

    @api.onchange('cashier_name')
    def setcashier(self):
        self.cashier = self.cashier_name.name

    def data_input_form_DB(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 團員眷屬檔')
        i = 1
        for line in lines:
            _logger.error(' %s / %s', i, len(lines))
            self.create({
                'w_id': line[u'團員編號'],
                'number': line[u'序號'],
                'name': line[u'姓名'],
                'cellphone': line[u'手機'],
                'con_addr': line[u'通訊地址'],
                'con_phone': line[u'電話一'],
                'con_phone2': line[u'電話二'],
                'zip_code': line[u'郵遞區號'],
                'type': 1,
                'habbit_donate': self.check_habbit(line[u'捐助種類編號']),
                'rec_send': self.checkbool(line[u'收據寄送']),
                'is_donate': self.checkbool(line[u'是否捐助']),
                'self': line[u'自訂排序'],
                'key_in_user': self.check_user(line[u'輸入人員']),
                'birth': self.check_db_date(line[u'建檔日期']),
                'db_chang_date': self.check(line[u'異動日期'])
            })
            i += 1

    def check_habbit(self, habbit):
        if habbit == u'01':
            return 01
        elif habbit == u'02':
            return 02
        elif habbit == u'03':
            return 03
        elif habbit == u'04':
            return 04
        elif habbit == u'05':
            return 05
        elif habbit == u'06':
            return 06
        elif habbit == u'99':
            return 99
        else:
            return None

    # 生日裡面有亂放東西，需要驗證是否真的是YYYY-MM-DD的格式
    def check_db_date(self, date):
        if date:
            try:
                time.strptime(date, "%Y-%m-%d")
                return date
            except:
                return None
        else:
            return None

    def check_user(self, row):
        check = self.env['c.worker'].search([('w_id', '=', row)])
        if check.id > 0:
            return check.id
        else:
            return False

    def set_parent(self):
        self.search([]).remove()


    # def set_parent(self):
    #     member = self.search([('w_id', '!=', None), ('number', '=', '1')])
    #     conn = psycopg2.connect("dbname=old_cdg user=odoo password=odoo")
    #     cur = conn.cursor()
    #     i = 1
    #     for line in member:
    #         # try:
    #         sql = "UPDATE normal_p SET parent = '{}' WHERE w_id = '{}' AND number != '1'".format(str(line.id),
    #                                                                                              str(line.w_id))
    #         _logger.error('it is run to %s line', i)
    #         cur.execute(sql)
    #         # except Exception:
    #         #     _logger.error('it is run to %s line', i)
    #         #     pass
    #         i += 1
    #     conn.commit()
    #     cur.close()
    #     conn.close()

    def data_input_from_database(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 團員檔')
        i = 1
        for line in lines:
            _logger.error(' %s / %s', i, len(lines))
            exist = False
            member = self.search([('w_id', '=', line[u'團員編號']), ('number', '=', '1'), ('name', '=', line[u'姓名'])])
            if member.id > 0:
                exist = True
            if exist is False and member.special_tag is not True:
                id_create = self.create({
                    'special_tag': True,
                    'w_id': line[u'團員編號'],
                    'number': u'0',
                    'name': line[u'姓名'],
                    'birth': self.check(line[u'出生日期']),
                    'cellphone': line[u'手機'],
                    'zip_code':line[u'郵遞區號'],
                    'con_addr': line[u'通訊地址'],
                    'con_phone': line[u'電話一'],
                    'con_phone2': line[u'電話二'],
                    'donate_cycle': line[u'捐助週期'],
                    'ps2': line[u'備註'],
                    'rec_send': self.checkbool(line[u'收據寄送']),
                    'bank_id': line[u'扣款銀行代碼'],
                    'bank_id2': line[u'扣款分行代碼'],
                    'thanks_send': self.checkbool(line[u'感謝狀寄送']),
                    'report_send': self.checkbool(line[u'報表寄送']),
                    'bank_check': self.checkbool(line[u'銀行核印']),
                    'cashier': line[u'收費員編號'],
                    'build_date': self.check_db_date(line[u'建檔日期']),
                    'db_chang_date': self.check(line[u'異動日期']),
                    'key_in_user': self.check_user(line[u'輸入人員']),
                })

            i += 1

    def check(self, date_check):
        if date_check:
            return date_check
        else:
            return None

    def checkbool(self, bool):
        if bool == 'Y':
            return True
        elif bool == 'N':
            return False

    def set_consultant(self):
        sql =" INSERT INTO member_data(member_id,name,birthday,user_id,cellphone,phone1,phone2,reg_zip_code,reg_address,conn_zip_code,conn_address,description,clerk_id,rec_send,print_note,self_order,normal_p_id, member_type) "\
             " SELECT 會員編號, 姓名, case when 出生日期='' then NULL else cast(出生日期 as date) end as 出生日期, 身份證號, 手機, 電話一, 電話二, 戶籍郵遞區號, 戶籍通訊地址, 郵遞區號, 通訊地址, 備註, 收費員編號, case when 收據寄送='N' then FALSE else TRUE end as 收據寄送, case when 名冊列印='N' then FALSE else TRUE end as 名冊列印, 自訂排序, b.id, 會員種類編號  FROM 會員檔 a"\
             " INNER JOIN normal_p b on a.姓名=b.name and a.戶籍通訊地址=b.con_addr"
        self._cr.execute(sql)
        return True
    def set_member(self):
        sql ="INSERT INTO member_data(adviser_id,name,cellphone,phone1,phone2,reg_zip_code,reg_address,conn_zip_code,conn_address,advise_date,description,clerk_id,rec_send,report_send,thanks_send,self_order,normal_p_id) "\
             " SELECT 顧問編號, 姓名, 手機, 電話一, 電話二, 戶籍郵遞區號, 戶籍通訊地址, 郵遞區號, 通訊地址,case when 聘顧日期='' then NULL else cast(聘顧日期 as date) end as 聘顧日期, 備註, 收費員編號, case when 收據寄送='N' then FALSE else TRUE end as 收據寄送, case when 報表寄送='N' then FALSE else TRUE end as 報表寄送, case when 感謝狀寄送='N' then FALSE else TRUE end as 感謝狀寄送, 自訂排序, b.id FROM 顧問檔 a"\
             " INNER JOIN normal_p b on a.姓名=b.name and a.戶籍通訊地址=b.con_addr"
        self._cr.execute(sql)
        return True
    def start_mamber_batch(self):
        data = self.env['associatemember.fee'].search([])
        data.create({

            'year':self.year,
            'fee_code':'F120100081',
            'fee_payable':1200,
            'fee_date':'2017-12-20',
            'clerk_id':150,
            'normal_p_id':754514
        })
        return True
    def start_consultant_batch(self):
        data = self.env['consultant.fee'].search([])
        data.create({
            'year':self.year,
            'fee_code':'F1201000xx',
            'fee_payable':10000,
            'fee_date':'2017-12-20',
            'clerk_id':150,
            'normal_p_id': 761747
        })
        return True

#
# class DonateFamily(models.Model):
#     _name = 'donate.family'
#
#     name = fields.Char(string='眷屬姓名')
#     birth = fields.Date(string='生日')
#     cellphone = fields.Char(string='手機')
#     con_phone = fields.Char(string='聯絡電話(一)')
#     con_phone2 = fields.Char(string='聯絡電話(二)')
#     rec_address = fields.Char(string='收據地址')
#     habbit_donate = fields.Selection(selection=[(1,'造橋'),(2,'補路'),(3,'施棺'),(4,'伙食費'),(5,'窮困扶助'),(6,'其他工程')],string='喜好捐款種類')
#     self = fields.Char(string='自訂排序')
#     rec_send = fields.Selection(selection=[(1,'單獨'),(2,'合併')],string='收據寄送')
#     now_donate = fields.Boolean(string='目前是否捐助' ,default= True)
