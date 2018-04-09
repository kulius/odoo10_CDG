# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CoffinDonation(models.Model):
    _name = 'coffin.donation'

    name = fields.Char(string='捐款者姓名', related='donate_order_id.donate_member.name')
    donate = fields.Integer(string='施棺捐款金額', related='donate_order_id.donate')
    donate_price = fields.Integer(string='施棺捐款金額(已用)', related='donate_order_id.used_money')
    use_amount = fields.Boolean(string='施棺捐款是否已支用', related='donate_order_id.use_amount')
    available_balance = fields.Integer(string='可用餘額', related='donate_order_id.available_balance')
    donate_date = fields.Date(string='捐款日期',related='donate_order_id.donate_date')
    accumulated_amount = fields.Integer(string='累積金額', related='coffin_donation_id.donate_price')
    donate_apply_price = fields.Integer(string='申請金額', related='coffin_donation_id.donate_apply_price')

    coffin_donation_id = fields.Many2one(comodel_name='coffin.base')
    old_coffin_donation_id = fields.Many2one(comodel_name='coffin.base')
    # donate_single_id = fields.Many2one(comodel_name='donate.single', string='捐款編號')
    donate_order_id = fields.Many2one(comodel_name='donate.order', string='捐款者 (可用餘額)' , domain=[('donate_type', '=', 3),('available_balance', '>=', 5000)])
    donate_id =  fields.Char(string='捐款編號', related='donate_order_id.donate_id')

    @api.onchange('donate_order_id')
    def set_used_money(self): # 改在這裡
        basic_setting = self.env['ir.config_parameter'].search([])
        if self.donate_apply_price == 0:  # 如果申請金額沒有填入特定的施棺滿足額, 則自動預設為基本設定檔的施棺滿足額
            for line in basic_setting:  # 讀取基本設定檔的施棺滿足額
                if line.key == 'coffin_amount':
                    self.donate_apply_price = int(line.value)

        if self.donate_order_id:
            if self.coffin_donation_id.coffin_date < self.donate_order_id.donate_date:
                raise ValidationError(u'捐款者捐款日期不得晚於領款日期')

            Cumulative_amount = self.donate_apply_price - self.accumulated_amount # 捐款金額減掉累積金額的差額, 也就是還差多少錢可以滿30000
            if self.available_balance - Cumulative_amount > 0 : # 捐款者的款金額大於目前施棺的差額
                self.available_balance = self.available_balance - Cumulative_amount #  捐款者的捐款金額扣掉差額, 剩下的錢返回捐款者帳戶
                self.donate_price = Cumulative_amount # 差額寫入donate_order 的已用金額欄位
                self.use_amount = False # 此筆捐款尚未使用完畢
            elif self.available_balance - Cumulative_amount <= 0 : # 代表此筆捐款金額無法滿足目前的施棺差額
                self.donate_price = self.available_balance # 捐款金額的可用餘額寫入 donate_order 已用金額欄位
                self.available_balance = 0 # 此筆金額全數支用完畢
                self.use_amount = True # 此筆金額全數支用完畢

    def data_input_from_database(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 施棺捐款檔')
        for line in lines:
            id_create = self.create({
                'coffin_id': line[u'施棺編號'],
                'donate_id':line[u'捐款編號'],
                'donate_price':line[u'捐款金額'],
            })