# -*- coding: utf-8 -*-
import time

from odoo import models, fields, api

#一般人基本檔 團員 會員 收費員 顧問
import logging

_logger = logging.getLogger(__name__)

class NormalP(models.Model):
    _name = 'normal.p'

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
    key_in_user = fields.Many2one(comodel_name='c.worker',string='輸入人員')
    db_chang_date = fields.Date(string='異動日期')
    build_date = fields.Date(string='建檔日期')

    email = fields.Char(string='Email')
    type = fields.Many2many(comodel_name='people.type', string='人員種類')
    self_iden = fields.Char(string='身分證字號')

    rec_addr = fields.Char(string='收據地址')
    con_addr = fields.Char(string='聯絡地址')
    send_addr = fields.Char(string='寄送地址')
    address = fields.Char(string='通訊地址')
    sex = fields.Selection(selection=[(1,'男生'),(2,'女生')],string='性別')
    come_date = fields.Date(string='到職日期')
    lev_date = fields.Date(string='離職日期')
    ps = fields.Text(string='備註')
    habbit_donate = fields.Selection(selection=[(1,'造橋'),(2,'補路'),(3,'施棺'),(4,'伙食費'),(5,'窮困扶助'),(6,'其他工程')],string='喜好捐款')
    cashier_name = fields.Many2one(comodel_name='c.worker',string='收費員姓名', domain="[('job_type', '=', '2'), ]")
    donate_cycle = fields.Selection(selection=[('03','季繳'),('06','半年繳'),('12','年繳')],string='捐助週期')
    rec_type = fields.Selection(selection=[(1,'正常'),(2,'年收據')],string='收據狀態')
    rec_send = fields.Boolean(string='收據寄送')
    is_donate = fields.Boolean(string='是否捐助')
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
    cashier = fields.Char(string='收費員')
    pay_date = fields.Date(string='收費日期')
    booklist = fields.Boolean(string='名冊列印')
    member_type = fields.Selection(selection=[(1, '基本會員'), (2, '贊助會員')], string='會員種類')
    hire_date = fields.Date(string='雇用日期')

    #來判斷你是不是老大
    parent = fields.Many2one(comodel_name='normal.p', string='戶長')
    donate_family1 = fields.One2many(comodel_name='normal.p',inverse_name='parent', string='團員眷屬')

    member_data_ids = fields.Many2one(comodel_name='member.data', string='關聯的顧問會員檔')

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
        new_id =""
        i = 1
        type_id =0
        for line in member_data:
            _logger.error(' %s / %s', i, len(member_data))
            if line.conn_zip_code !="":
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
            i = i+1
            max_id = max_id +1

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



    def check_habbit(self,habbit):
        if habbit == u'01':
            return 1
        elif habbit == u'02':
            return 2
        elif habbit == u'03':
            return 3
        elif habbit == u'04':
            return 4
        elif habbit == u'05':
            return 5
        elif habbit == u'99':
            return 6
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

    def check_user(self,row):
        check = self.env['c.worker'].search([('w_id','=',row)])
        if check.id >0:
            return check.id
        else:
            return False

    def set_parent(self):
        member = self.search([('new_coding','=',None)])
        i = 726050
        for line in member:
            _logger.error(' %s / %s', i-726050, len(member))
            line.write({
                'new_coding':u'000'+str(i)
            })
            i +=1



    def data_input_from_database(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 團員檔')
        i = 1
        for line in lines:
            _logger.error(' %s / %s', i, len(lines))
            exist = False
            member = self.search([('w_id', '=',line[u'團員編號']),('number','=','1'),('name','=',line[u'姓名'])])
            if member.id > 0:
                exist = True
            if exist is False and member.special_tag is not True:
                id_create = self.create({
                    'special_tag':True,
                    'w_id': line[u'團員編號'],
                    'number':u'0',
                    'name': line[u'姓名'],
                    'birth': self.check(line[u'出生日期']),
                    'cellphone': line[u'手機'],
                    'zip_code'
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
                    'bank_check':self.checkbool(line[u'銀行核印']),
                    'cashier':line[u'收費員編號'],
                    'build_date':self.check_db_date(line[u'建檔日期']),
                    'db_chang_date': self.check(line[u'異動日期']),
                    'key_in_user': self.check_user(line[u'輸入人員']),
                })

            i += 1

    def check(self,date_check):
        if date_check:
            return date_check
        else:
            return  None

    def checkbool(self,bool):
        if bool == 'Y':
            return True
        elif bool == 'N':
            return  False

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
