# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CoffinBase(models.Model):
    _name = 'coffin.base'

    name = fields.Char()
    coffin_id = fields.Char(string="施棺編號")
    donate_type = fields.Selection(selection=[('Z','零捐'),('A','累積')],string='捐助方式')
    coffin_date = fields.Date(string='施棺日期')
    coffin_date_year = fields.Char(string='年度')
    coffin_date_group = fields.Char(string='期別')
    user = fields.Char(string='受施者')
    geter = fields.Char(string='領款人')
    dealer = fields.Char(string='處理者')
    con_phone = fields.Char(string='聯絡電話(一)')
    con_phone2 = fields.Char(string='聯絡電話(二)')
    cellphone = fields.Char(string='手機')
    zip_code = fields.Char(string='郵遞區號')
    con_addr = fields.Char(string='通訊地址')
    donater_ps = fields.Text(string='捐款者備註')
    ps = fields.Text(string='備註')
    donate_price = fields.Char(string='累積金額')
    finish = fields.Boolean(string='是否結案')
    batch_donate = fields.One2many(comodel_name='coffin.donation',inverse_name='coffin_donation_id',string='捐助資料')
    create_date = fields.Date(string='建檔日期')

    def data_input_coffin(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 施棺檔')
        for line in lines:
            id_create2 = self.create({
                'coffin_id': line[u'施棺編號'],
                'donate_type': line[u'捐助方式'],
                'user': line[u'受施者'],
                'con_phone': line[u'電話一'],
                'con_phone2':line[u'電話二'],
                'cellphone':line[u'手機'],
                'geter': line[u'領款人'],
                'dealer':line[u'處理者'],
                'zip_code':line[u'郵遞區號'],
                'con_addr':line[u'通訊地址'],
                'coffin_date':self.check(line[u'施棺日期']),
                'create_date':self.check(line[u'建檔日期']),
                'db_chang_date':self.check(line[u'異動日期']),
                'finish':self.checkbool(line[u'結案']),
                'donate_price':line[u'已捐總額'],
                'coffin_date_year':line[u'年度'],
                'coffin_date_group':line[u'期別'],
            })
    def add_coffin_file(self):
        wizard_data = self.env['new.coffin'].create({
            'order_ids': self.coffin_id
        })

        action = self.env.ref('cdg_base.new_coffin_action').read()[0]
        action['res_id'] = wizard_data.id
        return True;

    def check_db_date(self, date):
        if date:
            try:
                time.strptime(date, "%Y-%m-%d")
                return date
            except:
                return None
        else:
            return None
    def checkbool(self,bool):
        if bool == 'Y':
            return True
        elif bool == 'N':
            return False

    def check(self,date_check):
        if date_check:
            return date_check
        else:
            return None

