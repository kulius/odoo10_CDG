# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import *
import datetime

class CoffinBase(models.Model):
    _name = 'coffin.base'
    _rec_name = 'coffin_id'
    _order = 'coffin_id desc'
    _description = u'施棺基本資料管理'

    name = fields.Char()
    coffin_id = fields.Char(string="施棺編號")
    donate_type = fields.Selection(selection=[('Z','零捐'),('A','累積')],string='捐助方式')
    coffin_date = fields.Date(string='領款日期',default=fields.Date.today)
    dead_date = fields.Date('死亡日期',default=fields.Date.today)
    coffin_date_year = fields.Char(string='年度',default=datetime.date.today().year - 1911)
    coffin_date_group = fields.Selection([(1,'01'),(2,'02'),(3,'03'),(4,'04')],'季別')
    coffin_season = fields.Char('期別')
    bank_account = fields.Char('匯款帳號')
    user = fields.Char(string='受施者')
    user_iden = fields.Char('受施者身份證字號')
    geter = fields.Char(string='領款人')
    geter_iden = fields.Char('領款者身份證字號')
    dealer = fields.Char(string='處理者')
    donor = fields.Char('捐款者', compute='get_donate_name')
    con_phone = fields.Char(string='聯絡電話')
    con_phone2 = fields.Char(string='聯絡電話(二)')
    cellphone = fields.Char(string='手機')
    zip_code = fields.Char(string='領款人郵遞區號') # 領款者地址 原通訊地址
    payee_addr = fields.Char('領款人地址')
    zip_code2 = fields.Char('受施者郵遞區號') #弔祭地址
    con_addr = fields.Char(string='受施者地址') #原通訊地址
    donater_ps = fields.Text(string='捐款者備註')
    ps = fields.Text(string='備註')
    donate_price = fields.Integer(string='累積金額')
    donate_apply_price = fields.Integer('申請金額',default=0)
    finish = fields.Boolean(string='是否結案')
    batch_donate = fields.One2many(comodel_name='coffin.donation',inverse_name='coffin_donation_id',string='捐助資料')
    old_batch_donate = fields.One2many(comodel_name='old.coffin.donation', inverse_name='old_coffin_donation_id', string='舊捐助資料')
    create_date = fields.Date(string='建檔日期')
    db_chang_date = fields.Date(string='異動日期')
    exception_case = fields.Boolean(string='特案處理')
    coffin_image = fields.One2many(comodel_name='coffin.image',inverse_name='case_code',string='施棺文件資料')

    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', ondelete='cascade')
    temp_key_in_user = fields.Char(string='輸入人員_temp')
    same_addr = fields.Boolean("領款人地址同受施者地址")

    @api.model
    def create(self, vals):
        res_id = super(CoffinBase, self).create(vals)
        if res_id.coffin_date < res_id.dead_date:
            raise ValidationError(u'領款日期不得早於死亡日期')

        array = []
        data = self.env['coffin.base'].search([('coffin_id','!=','Null')])
        for line in data:
            array.append(int(line.coffin_id))
        array.sort()
        res_id.coffin_id = array[len(array)-1] + 1

        return res_id

    @api.onchange('same_addr')
    def set_payee_addr(self):
        if self.same_addr == True:
            self.payee_addr = self.con_addr
        else:
            self.payee_addr = ""

    def coffin_batch(self,ids):
        res = []
        for line in ids:
            res.append([4, line])
        wizard_data = self.env['coffin.batch'].create({
            'coffin_data_lists': res
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'coffin.batch',
            'name': '批次處理',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    @api.onchange('batch_donate')
    def compute_money(self):
        if self.batch_donate or self.old_batch_donate:
            basic_setting = self.env['ir.config_parameter'].search([])
            if self.donate_apply_price == 0:  # 如果申請金額沒有填入特定的施棺滿足額, 則自動預設為基本設定檔的施棺滿足額
                for line in basic_setting:  # 讀取基本設定檔的施棺滿足額
                    if line.key == 'coffin_amount':
                        self.donate_apply_price = int(line.value)

            for line in self: # 從捐助資料表中, 計算目前的累積金額
                line.donate_price = 0
                if line.donate_apply_price == line.donate_price:
                    raise ValidationError(u'已達施棺滿足額')
                if line.batch_donate and len(line.old_batch_donate) == 0:
                    for row in line.batch_donate:
                        line.donate_price = int(float(line.donate_price)) + int(float(row.history_donate_records))
                elif line.old_batch_donate and line.finish == True:
                    for row in line.old_batch_donate:
                        line.donate_price = int(float(line.donate_price)) + int(float(row.donate_price))
                        line.donate_apply_price = int(line.donate_price)
            if self.donate_apply_price == self.donate_price:
                self.finish = True

    def compute_old_data(self):
        for i in self.search([]): # 搜尋 coffin_base 的每筆資料
            r =[]
            for line in i.old_batch_donate: # 撈出 coffin_base裡某一筆資料的舊捐助資料頁籤
                for row in line.donate_single_id.donate_list: # 撈出舊捐助資料頁籤裡的捐款編號 donate_single_id
                    order_ids ={
                        'donate_order_id': row.id
                    }
                    r.append([0,0,order_ids])
            i.write({
                'batch_donate': r
            })
        return True

    def add_coffin_file(self):
        default_price_flag = False # 判斷是否為基本設定檔的施棺滿足額
        temp_default_price = 0 # 暫存用的, 沒幹嘛
        big_donate_flag = False
        basic_setting = self.env['ir.config_parameter'].search([])
        if self.donate_apply_price == 0 and self.exception_case == False: # 如果申請金額沒有填入特定的施棺滿足額, 則自動預設為基本設定檔的施棺滿足額
            for line in basic_setting: # 讀取基本設定檔的施棺滿足額
                if line.key == 'coffin_amount':
                    self.donate_apply_price = int(line.value)
                    default_price_flag = True
        elif self.donate_apply_price != 0 and self.exception_case == False:
            for line in basic_setting: # 讀取基本設定檔的施棺滿足額
                if line.key == 'coffin_amount':
                    self.donate_apply_price = int(line.value)
                    default_price_flag = True
        else: # 如果有輸入申請金額, 則還是要讀取基本設定檔的施棺滿足額, 後續程式要判斷用
            for line in basic_setting:  # 讀取基本設定檔的施棺滿足額
                if line.key == 'coffin_amount':
                    temp_default_price = int(line.value)
                    default_price_flag = False

        for line in self.batch_donate: # 從捐助資料表中, 計算目前的累積金額
            self.donate_price = int(float(self.donate_price)) + int(float(line.donate_price))

        Cumulative_amount = self.donate_apply_price - int(float(self.donate_price)) #計算已累積金額與施棺滿足額的差額
        flag = False # 後續程式判讀使否結案用

        if Cumulative_amount == 0:  # 初始判斷累積金額是否已滿足施棺滿足額
            self.finish = True
            flag = True

        if self.finish == True: # 判斷該專案是否已結案
            raise ValidationError(u'已結案，無法再更改')
        elif self.finish == False:
            # if self.donate_price == 0  and default_price_flag == True and self.exception_case == False: # 沒有任何的捐助明細,而且確認申請金額是讀取基本設定檔的施棺滿足額, 而不是使用者自行輸入的特殊案例,
            #     lines = self.env['donate.order'].search([('donate_type', '=', 3),('available_balance', '=', self.donate_apply_price),('donate_date','<',self.coffin_date)], limit = 1)
            #     if lines: # 有單筆3萬元的捐助資料
            #         for line in lines:
            #             if Cumulative_amount == 0:  # 達到施棺滿足額
            #                 self.finish = True
            #                 flag = True
            #                 break
            #             if int(line.available_balance) == Cumulative_amount and flag == False: # 單筆 3萬元 的捐款優先使用
            #                 self.write({
            #                     'batch_donate': [(0, 0, {
            #                         'donate_order_id': line.id
            #                     })]
            #                 })
            #                 line.use_amount = True  # 確認已支用此筆施棺捐款金額
            #                 line.used_money = line.available_balance # 已用金額
            #                 self.donate_price = int(float(self.donate_price)) + line.available_balance  # 將捐款金額加入累積金額
            #                 Cumulative_amount = Cumulative_amount - line.available_balance  # 施棺滿足額 減掉 捐款額
            #                 line.available_balance = 0  # 該筆捐款的可用餘額歸 0
            #                 self.finish = True  # 結案
            #                 flag = True  # 結案
            #     if flag == False: # 沒有單筆三萬元的捐款, 找大於1萬元的捐款
            #         lines = self.env['donate.order'].search([('donate_type', '=', 3),('available_balance', '>=', 10000),('donate_date', '<', self.coffin_date)], limit= 3 )
            #         num = len(lines)
            #         if num >= 3:
            #             for line in lines:
            #                 if Cumulative_amount == 0:  # 達到施棺滿足額
            #                     self.finish = True
            #                     flag = True
            #                     break
            #                 if Cumulative_amount < 10000:
            #                     flag = False
            #                     break
            #                 if int(line.available_balance) == temp_default_price and line.donate_type == 3:  # 過濾單筆施棺捐款為3萬元的資料, 保險用的
            #                     continue
            #                 elif int(line.available_balance) <= Cumulative_amount and flag == False:  # 判斷 目前的施棺捐款額是否小於等於施棺滿足額的差額
            #                     self.write({
            #                         'batch_donate': [(0, 0, {
            #                             'donate_order_id': line.id
            #                         })]
            #                     })
            #                     line.use_amount = True  # 確認已支用此筆施棺捐款金額
            #                     line.used_money = line.available_balance # 已用金額
            #                     self.donate_price = int(float(self.donate_price)) + line.available_balance  # 將捐款金額加入累積金額
            #                     Cumulative_amount = Cumulative_amount - line.available_balance  # 施棺滿足額 減掉 捐款額
            #                     line.available_balance = 0  # 該筆捐款金額歸 0
            #
            # if self.donate_price != 0 or flag == False:  # 代表已有捐助資料 或 沒有單筆3萬元的資料
            #     for line in self.batch_donate:  # 從捐助資料表中, 計算目前的累積金額
            #         if int(float(line.donate_price)) >= 10000:
            #             big_donate_flag = True
            #     if big_donate_flag and self.exception_case == False:
            #         lines = self.env['donate.order'].search([('donate_type', '=', 3), ('available_balance', '>=', 10000), ('use_amount', '=', False),('donate_date', '<', self.coffin_date)])
            #         for line in lines:
            #             if Cumulative_amount == 0:  # 達到施棺滿足額
            #                 self.finish = True
            #                 flag = True
            #                 break
            #             if Cumulative_amount < 10000:
            #                 flag = False
            #                 break
            #             if int(line.available_balance) == temp_default_price and line.donate_type == 3:  # 過濾單筆施棺捐款為3萬元的資料, 保險用的
            #                 continue
            #             elif int(line.available_balance) <= Cumulative_amount and flag == False:  # 判斷 目前的施棺捐款額是否小於等於施棺滿足額
            #                 self.write({
            #                     'batch_donate': [(0, 0, {
            #                         'donate_order_id': line.id
            #                     })]
            #                 })
            #                 line.use_amount = True  # 確認已支用此筆施棺捐款金額
            #                 line.used_money = line.available_balance # 已用金額
            #                 self.donate_price = int(float(self.donate_price)) + line.available_balance  # 將捐款金額加入累積金額
            #                 Cumulative_amount = Cumulative_amount - line.available_balance  # 施棺滿足額 減掉 捐款額
            #                 line.available_balance = 0  # 該筆捐款金額歸 0
            #     else:
            lines = self.env['donate.order'].search([('donate_type', '=', 3),('available_balance', '<', 5000),('use_amount', '=', False),('donate_date','<',self.coffin_date)],order="donate_date")
            if lines and flag == False:
                for line in lines:
                    if Cumulative_amount == 0:  # 達到施棺滿足額
                        self.finish = True
                        flag = True
                        break

                    if int(line.available_balance) <= Cumulative_amount and flag == False:  # 判斷 目前的施棺捐款額是否小於等於施棺滿足額
                        self.write({
                            'batch_donate': [(0, 0, {
                                'donate_order_id': line.id,
                                'history_donate_records':line.available_balance,
                                'normal_p_id':line.donate_member.id
                            })]
                        })
                        line.use_amount = True  # 確認已支用此筆施棺捐款金額
                        line.used_money = line.used_money + line.available_balance # 已用金額
                        self.donate_price = int(float(self.donate_price)) + line.available_balance  # 將捐款金額加入累積金額
                        Cumulative_amount = Cumulative_amount - line.available_balance  # 施棺滿足額 減掉 捐款額
                        line.available_balance = 0  # 該筆捐款金額歸 0


                    elif int(line.available_balance) > Cumulative_amount and flag == False:  # 單筆捐款大於施棺滿足額的差額
                        self.write({
                            'batch_donate': [(0, 0, {
                                'donate_order_id': line.id,
                                'history_donate_records': line.available_balance - (line.available_balance - Cumulative_amount),
                                'normal_p_id': line.donate_member.id
                            })]
                        })
                        line.used_money = line.used_money + line.available_balance - (line.available_balance - Cumulative_amount) # 已用金額
                        line.available_balance = line.available_balance - Cumulative_amount # 捐款金額減掉施棺滿足額的差額, 再把餘額寫回可用餘額之中
                        self.donate_price = int(float(self.donate_price)) + Cumulative_amount
                        Cumulative_amount = 0 # 達到施棺滿足額, 所以差額歸0
                        line.use_amount = False

        if Cumulative_amount != 0:
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

    @api.depends('batch_donate.donate_order_id')
    def get_donate_name(self):
        for i in self:
            donate_number = 0  # 紀錄捐款筆數
            str_build = ''
            if i.donater_ps:
                str_build = i.donater_ps
                i.donor = str_build
            elif i.batch_donate:
                for line in i.batch_donate:
                    donate_number += 1
                    if donate_number <= 6:
                        if line.donate_order_id.donate_member.name == False:
                            str_build += u'無名氏' + ', '
                        else:
                            str_build += line.donate_order_id.donate_member.name + ', '
                    elif donate_number > 6:
                        str_build = u"眾善士"
                i.donor = str_build.rstrip(', ')
            elif i.old_batch_donate:
                for line in i.old_batch_donate:
                    donate_number += 1
                    if donate_number <= 6:
                        if line.donor:
                          str_build += line.donor + ', '
                        else:
                          continue
                    elif donate_number > 6:
                        str_build = u"眾善士"
                i.donor = str_build.rstrip(', ')



    @api.onchange('coffin_date', 'dead_date')
    def compare_date(self):
        if self.coffin_date < self.dead_date:
            raise ValidationError(u'領款日期不得早於死亡日期')
        if len(str(datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').year - 1911)) < 3 : # 民國100年之前的資料, 將年份補足為三位數, 並將年份帶入施棺期別的年份
            self.coffin_date_year = '0' + str(datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').year - 1911)
        elif len(str(datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').year - 1911)) == 3 : # 將領款日期的年份帶入施棺期別的年份
            self.coffin_date_year = datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').year - 1911
        # self.coffin_date_group = datetime.strptime(self.coffin_date, '%Y-%m-%d').month # 領款日期的月份帶入施棺期別的月份

        if(datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 1 or datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 2 or datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 3):
            self.coffin_date_group = 1
        elif (datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 4 or datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 5 or datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 6):
            self.coffin_date_group = 2
        elif (datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 7 or datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 8 or datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 9):
            self.coffin_date_group = 3
        elif (datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 10 or datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 11 or datetime.datetime.strptime(self.coffin_date, '%Y-%m-%d').month == 12):
            self.coffin_date_group = 4

    @api.onchange('exception_case')
    def set_exception(self):
        if self.exception_case is True:
            basic_setting = self.env['ir.config_parameter'].search([])
            for line in basic_setting: # 讀取基本設定檔的施棺滿足額
                if line.key == 'exception_coffin_amount':
                    self.donate_apply_price = int(line.value)

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


class OldCoffinDonation(models.Model):
    _name = 'old.coffin.donation'

    coffin_id = fields.Char(string='施棺編號')
    donate_id = fields.Char(string='捐款編號')
    donate_price = fields.Integer(string='施棺捐款金額')

    old_coffin_donation_id = fields.Many2one(comodel_name='coffin.base')
    donate_single_id = fields.Many2one(comodel_name='donate.single', string='捐款編號')
    normal_p_id = fields.Many2one(comodel_name='normal.p')
    donate_date = fields.Date(string='捐款日期', related='donate_single_id.donate_date')
    coffin_user = fields.Char(string='受施者', related='old_coffin_donation_id.user')
    coffin_date = fields.Date(string='領款日期', related='old_coffin_donation_id.coffin_date')
    donor = fields.Char(string='捐款者')