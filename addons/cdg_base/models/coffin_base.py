# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class CoffinBase(models.Model):
    _name = 'coffin.base'

    name = fields.Char()
    coffin_id = fields.Char(string="施棺編號")
    donate_type = fields.Selection(selection=[('Z','零捐'),('A','累積')],string='捐助方式')
    coffin_date = fields.Date(string='領款日期',default=datetime.today())
    coffin_date_year = fields.Char(string='年度',default=datetime.today().year)
    coffin_date_group = fields.Selection([(1,'01'),(2,'02'),(2,'02'),(3,'03'),(4,'04'),(5,'05'),(6,'06'),(7,'07'),(8,'08'),(9,'09'),(10,'10'),(11,'11'),(12,'12')],'月份',default = 1)
    coffin_season = fields.Char('期別')
    bank_account = fields.Char('匯款帳號')
    user = fields.Char(string='受施者')
    user_iden = fields.Char('受施者身份證字號')
    geter = fields.Char(string='領款者')
    geter_iden = fields.Char('領款者身份證字號')
    dealer = fields.Char(string='處理者')
    donor = fields.Char('捐款者')
    con_phone = fields.Char(string='聯絡電話(一)')
    con_phone2 = fields.Char(string='聯絡電話(二)')
    cellphone = fields.Char(string='手機')
    zip_code = fields.Char(string='郵遞區號') # 領款者地址 原通訊地址
    zip_code2 = fields.Char('郵遞區號') #弔祭地址
    con_addr = fields.Char(string='領款者地址') #原通訊地址
    dead_addr = fields.Char('弔祭地址')
    donater_ps = fields.Text(string='捐款者備註')
    ps = fields.Text(string='備註')
    donate_price = fields.Integer(string='累積金額')
    donate_apply_price = fields.Integer('申請金額')
    finish = fields.Boolean(string='是否結案')
    batch_donate = fields.One2many(comodel_name='coffin.donation',inverse_name='coffin_donation_id',string='捐助資料',compute='get_donate_name')
    old_batch_donate = fields.One2many(comodel_name='coffin.donation', inverse_name='old_coffin_donation_id', string='舊捐助資料')

    donate_single_id = fields.Many2one(comodel_name='donate.single', string='捐款編號')
    create_date = fields.Date(string='建檔日期')
    db_chang_date = fields.Date(string='異動日期')

    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', ondelete='cascade')
    temp_key_in_user = fields.Char(string='輸入人員_temp')

    def add_coffin_file(self):
        lines = self.env['donate.order'].search([('donate_type', '=', '3'),('use_amount','=',False)]) # 從捐款明細中, 搜尋所有施棺捐款的資料, 並依最大筆金額進行排序
        basic_setting = self.env['ir.config_parameter'].search([])
        coffin_amount = 0
        for line in basic_setting: # 讀取基本設定檔的施棺滿足額
            if line.key == 'coffin_amount':
                coffin_amount = int(line.value)


        # for line in self: # 從捐助資料表中, 計算目前的累積金額
        #     for row in line.batch_donate:
        #         line.donate_price = int(float(line.donate_price)) + int(float(row.donate_price))

        Cumulative_amount = coffin_amount - int(float(self.donate_price)) #計算已累積金額與施棺滿足額的差額
        flag = False

        if self.finish == True:
            raise ValidationError(u'已結案，無法再更改')
        elif self.finish == False:
            for line in lines:
                if int(self.donate_price) == Cumulative_amount: # 初始判斷累積金額是否已滿足施棺滿足額
                    self.finish = True
                    flag = True

                if int(line.donate) <= Cumulative_amount and flag == False: #判斷 目前的施棺捐款額是否小於等於施棺滿足額
                    self.write({
                        'batch_donate': [(0, 0, {
                            'donate_single_id': line.id
                        })]
                    })
                    line.use_amount = True # 確認已支用此筆施棺捐款金額
                    self.donate_price = int(float(self.donate_price)) + line.donate # 將捐款金額加入累積金額
                    Cumulative_amount = Cumulative_amount - line.donate # 施棺滿足額 減掉 捐款額
                if Cumulative_amount == 0: # 達到施棺滿足額
                    self.finish = True
                    flag = True
            if Cumulative_amount != 0: # 搜尋完所有的施棺捐款後, 仍然無法湊足施棺滿足額
                raise ValidationError(u'無法湊足施棺滿足額')
        return True;

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
                'coffin_date':self.check(line[u'領款日期']),
                'create_date':self.check(line[u'建檔日期']),
                'db_chang_date':self.check(line[u'異動日期']),
                'finish':self.checkbool(line[u'結案']),
                'donate_price':line[u'已捐總額'],
                'coffin_date_year':line[u'年度'],
                'coffin_date_group':line[u'期別'],
            })

    # #眾善士顯示目前由於是onchange 新增的時候會產生錯誤訊息
    # @api.depends('batch_donate')
    # def get_donate_name(self):
    #     lines = self.env['donate.order'].search([('donate_id', '!=', ''), ('donate', '!=', 0), ('donate_type', '=', '3'), ('use_amount', '=', False)],order='donate desc')  # 從捐款明細中, 搜尋所有施棺捐款的資料, 並依最大筆金額進行排序
    #     donate_number = 0  # 紀錄捐款筆數
    #     if (self.donater_ps != ''): #施棺捐款者備註為最高
    #         self.donor = self.donater_ps
    #     else:
    #         for line in lines:
    #             donate_number += 1
    #             if (donate_number < 6):
    #                 self.donor += line.donate_member.name
    #             elif (donate_number >= 6):
    #                 self.donor = "眾善士"

    @api.onchange('coffin_date_group')
    def compute_coffin_season(self):
        if(self.coffin_date_group == 1 or self.coffin_date_group == 2 or self.coffin_date_group == 3):
            self.coffin_season = '01'
        elif(self.coffin_date_group == 4 or self.coffin_date_group == 5 or self.coffin_date_group == 6):
            self.coffin_season = '02'
        elif (self.coffin_date_group == 7 or self.coffin_date_group == 8 or self.coffin_date_group == 9):
            self.coffin_season = '03'
        elif (self.coffin_date_group == 10 or self.coffin_date_group == 11 or self.coffin_date_group == 12):
            self.coffin_season = '04'

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