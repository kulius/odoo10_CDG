# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging, time

_logger = logging.getLogger(__name__)


class MemberData(models.Model):
    _name = 'member.data'
    _rec_name = 'name'
    _description = 'New Description'

    member_id = fields.Char(string='舊會員編號')
    adviser_id = fields.Char(string='舊顧問編號')
    name = fields.Char(string='姓名')
    user_id = fields.Char(string='身份證號')
    birthday = fields.Date(string='出生日期')
    cellphone = fields.Char(string='手機')
    phone1 = fields.Char(string='電話一')
    phone2 = fields.Char(string='電話一')
    reg_zip_code = fields.Char(string='戶籍郵遞區號')
    reg_address = fields.Char(string='戶籍通訊地址')
    conn_zip_code = fields.Char(string='郵遞區號')
    conn_address = fields.Char(string='通訊地址')
    member_type = fields.Char(string='會員種類')
    #member_type = fields.Many2many(comodel_name='people.type', string='會員種類')
    advise_date = fields.Date(string='聘僱日期(顧問才有)')
    build_date = fields.Date(string='建檔日期')
    db_chang_date = fields.Date(string='異動日期')
    description = fields.Text(string='備註')
    clerk_id = fields.Char(string='收費員編號')
    rec_send = fields.Boolean(string='收據寄送')
    thanks_send = fields.Boolean(string='感謝狀寄送(顧問才有)')
    print_note = fields.Boolean(string='名冊列印', default=True)
    report_send = fields.Boolean(string='收據寄送(顧問才有)')
    self_order = fields.Char(string='自訂排序')
    worker_id = fields.Many2one(comodel_name='c.worker', string='輸入人員')
    normal_p_id = fields.Many2one(comodel_name='normal.p', string='捐款名冊')

    def data_input_form_DB(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 會員檔')
        i = 1
        for line in lines:
            _logger.error(' %s / %s', i, len(lines))
            self.create({
                'member_id': line[u'會員編號'],
                'name': line[u'姓名'],
                'user_id': line[u'身份證號'],
                'birthday': self.check_db_date(line[u'出生日期']),
                'cellphone': line[u'手機'],
                'phone1': line[u'電話一'],
                'phone2': line[u'電話二'],
                'reg_zip_code': line[u'戶籍郵遞區號'],
                'reg_address': line[u'戶籍通訊地址'],
                'conn_zip_code': line[u'郵遞區號'],
                'conn_address': line[u'通訊地址'],
                'member_type':self.set_type(line[u'會員種類編號']),
                'build_date': self.check_db_date(line[u'建檔日期']),
                'db_chang_date': self.check_db_date(line[u'異動日期']),
                'description': line[u'備註'],
                'clerk_id': line[u'收費員編號'],
                'rec_send': self.checkbool(line[u'收據寄送']),
                'print_note': self.checkbool(line[u'名冊列印']),

                'self_order': line[u'自訂排序'],
                'worker_id': self.check_user(line[u'輸入人員']),

            })
            i += 1

    def data_input_form_DB2(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 顧問檔')
        i = 1
        for line in lines:
            _logger.error(' %s / %s', i, len(lines))
            self.create({
                'adviser_id': line[u'顧問編號'],
                'name': line[u'姓名'],
                'birthday': self.check_db_date(line[u'出生日期']),
                'cellphone': line[u'手機'],
                'phone1': line[u'電話一'],
                'phone2': line[u'電話二'],
                'reg_zip_code': line[u'戶籍郵遞區號'],
                'reg_address': line[u'戶籍通訊地址'],
                'conn_zip_code': line[u'郵遞區號'],
                'conn_address': line[u'通訊地址'],
                'member_type': [(4, 4)],
                'advise_date':self.check_db_date(line[u'聘顧日期']),
                'build_date': self.check_db_date(line[u'建檔日期']),
                'db_chang_date': self.check_db_date(line[u'異動日期']),
                'description': line[u'備註'],
                'clerk_id': line[u'收費員編號'],
                'rec_send': self.checkbool(line[u'收據寄送']),
                'report_send': self.checkbool(line[u'報表寄送']),
                'thanks_send': self.checkbool(line[u'感謝狀寄送']),
                'self_order': line[u'自訂排序'],
                'worker_id': self.check_user(line[u'輸入人員']),

            })
            i += 1

    def set_type(self,type):
        if type == u'06':
            return [(4, 3)]
        elif type == u'01':
            return [(4, 2)]
        else:
            return None

    def check_db_date(self, date):
        if date:
            try:
                time.strptime(date, "%Y-%m-%d")
                return date
            except:
                return None
        else:
            return None

    def checkbool(self, bool):
        if bool == 'Y':
            return True
        elif bool == 'N':
            return False

    def check_user(self,row):
        check = self.env['c.worker'].search([('w_id','=',row)])
        if check.id > 0 :
            return check.id
        else:
            return None