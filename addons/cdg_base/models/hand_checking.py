# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HandChecking(models.Model):
    _name = 'hand.checking'

    name = fields.Char()
    book_id = fields.Char(string='簿冊編號')
    #owner = fields.Many2one(comodel_name='c.worker',string='領取人', domain="[('job_type', '=', 2), ]")
    owner = fields.Char(string='領取人')
    own_date = fields.Date(string='領取日期')
    back_date = fields.Date(string='回收日期')
    back_account = fields.Char(string='回收金額')
    create_date1 = fields.Date(string='建檔日期')
    key_total_account = fields.Char(string='鍵入總金額')
    key_in_total = fields.One2many(comodel_name='hand.book',inverse_name='hand_book',string='鍵入總筆數')
    change_date = fields.Date(string='異動日期')

    take_money = fields.Char(string='已收金額')
    ps = fields.Text(string='備註')

    def data_input_hand_checking(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 手寫簿冊檔')
        for line in lines:
            id_create2 = self.create({
                'book_id':line[u'簿冊編號'],
                'owner':line[u'領取人'],
                'own_date':self.check(line[u'領取日期']),
                'back_date':self.check(line[u'回收日期']),
                'back_account':line[u'已收總金額'],
                'create_date1':self.check(line[u'建檔日期']),
                'ps':line[u'備註'],
                'change_date':self.check(line[u'異動日期']),
            })


    def check(self,date_check):
        if date_check:
            return date_check
        else:
            return  None

class HandBook(models.Model):
    _name = 'hand.book'

    donate_id = fields.Char(string='捐款編號')
    name = fields.Char(string='捐款人姓名')
    donate_money = fields.Char(string='捐款總額')
    donate_date = fields.Date(string='捐款日期')
    donate_type = fields.Selection(selection=[(1,'造橋'),(2,'補路'),(3,'施棺'),(4,'伙食費'),(5,'窮困扶助'),(6,'其他工程')],string='捐款項目')
    ps = fields.Text(string='備註')
    hand_book = fields.Many2one(comodel_name='hand.checking',string='屬於哪本簿子')