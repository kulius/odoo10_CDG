# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api
import datetime

#員工基本檔

class CWorker(models.Model):
    _name = 'c.worker'
    _description = u'員工基本資料管理'

    w_id = fields.Char(string='員工編號')
    employee_id = fields.Char(string='新員工編號')
    name = fields.Char(string='姓名')
    con_phone = fields.Char(string='連絡電話')
    con_phone2 = fields.Char(string='連絡電話(二)')
    cellphone = fields.Char(string='手機')
    email = fields.Char(string='Email')
    create_date1 = fields.Date(string='建檔日期')
    now_job = fields.Char(string='現在職稱')
    job_type = fields.Selection(selection=[(1,'一般員工'),(2,'收費員')],string='員工種類')


    self_iden = fields.Char(string='身分證字號')
    birth = fields.Date(string='出生日期')
    con_addr = fields.Char(string='通訊地址')
    sex = fields.Selection(selection=[('M','男生'),('F','女生')],string='性別')
    come_date = fields.Date(string='到職日期')
    lev_date = fields.Date(string='離職日期')
    highest_stu = fields.Char(string='最高學歷')
    ps = fields.Text(string='備註')
    zip_code = fields.Char(string='郵遞區號')
    db_chang_date = fields.Date(string='異動日期')

    normal_cash = fields.One2many(comodel_name='normal.p', inverse_name='cashier_name',string='捐款人繳費名冊') # 無法下domain在裡面
  #  normal_cash1 = fields.One2many(comodel_name='normal.p', string='捐款人繳費名冊')
    #member_cash = fields.One2many(comodel_name='normal.p',inverse_name='cashier_member_name',string='會員繳費名冊')
  #   consultant_cash1 = fields.One2many(comodel_name='normal.p', string='顧問繳費名冊')
  #   consultant_cash = fields.One2many(comodel_name='normal.p',inverse_name='cashier_name',string='顧問繳費名冊')

    @api.model
    def create(self, vals):

        res_id = super(CWorker, self).create(vals)

        self.env['res.users'].create({
            'login': res_id.w_id,
            'password': res_id.w_id,
            'name': res_id.name,
        })

        return res_id

    @api.multi
    def write(self,vals):
        c_worker = self.env['res.users'].search([('login', '=', self.w_id)])
        res = super(CWorker, self).write(vals)
        c_worker.partner_id.name = self.name
        c_worker.login = self.w_id
        return res

    def data_input_from_database(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 員工檔')
        for line in lines:
            id_create = self.create({
                'w_id': line[u'員工編號'],
                'name': line[u'姓名'],
                'sex': line[u'性別'],
                'birth':self.check(line[u'出生日期']),
                'self_iden': line[u'身份證號'],
                'cellphone': line[u'手機'],
                'now_job': line[u'電話一'],
                'con_phone2': line[u'電話二'],
                'con_addr': line[u'通訊地址'],
                'job': line[u'職稱'],
                'email':line[u'EMAIL'],
                'highest_stu':line[u'最高學歷'],
                'come_date': self.check(line[u'到職日期']),
                'create_date1': self.check(line[u'建檔日期']),
                'lev_date': self.check(line[u'離職日期']),
                'job_type': 1,
            })

    def data_input_cashier(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 收費員檔')
        for line in lines:
            id_create2 = self.create({
                'w_id': line[u'收費員編號'],
                'name': line[u'姓名'],
                'self_iden': line[u'身份證號'],
                'con_phone': line[u'電話一'],
                'con_phone2':line[u'電話二'],
                'cellphone':line[u'手機'],
                'zip_code': line[u'郵遞區號'],
                'con_addr':line[u'通訊地址'],
                'create_date':self.check_db_date(line[u'建檔日期']),
                'ps': line[u'備註'],
               # 'db_chang_date':self.check_db_date(line[u'異動日期']),
                'job_type': 2,
            })

    def change_password(self):
        print 'yes'

    def check_db_date(self, date):
        if date:
            try:
                time.strptime(date, "%Y-%m-%d")
                return date
            except:
                return None
        else:
            return None

    def check(self,date_check):
        if date_check:
            return date_check
        else:
            return  None

