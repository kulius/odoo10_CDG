# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DonorSearch(models.Model):
    _name = 'donor.search'

    # 方法與變數的名稱不能一樣

    is_Taiwan = fields.Boolean('全台灣')
    is_North = fields.Boolean('北部地區')
    is_Central = fields.Boolean('中部地區')
    is_South = fields.Boolean('南部地區')
    is_East = fields.Boolean('東部地區')

    is_Taipei = fields.Boolean('台北市')
    is_Keelung = fields.Boolean('基隆市')
    is_Xinbei = fields.Boolean('新北市')
    is_Taoyuan = fields.Boolean('桃園市')
    is_Hsinchu = fields.Boolean('新竹市')
    is_Hsinchu2 = fields.Boolean('新竹縣')
    is_Taichung = fields.Boolean('台中市')
    is_Changhua = fields.Boolean('彰化縣')
    is_Yunlin = fields.Boolean('雲林縣')
    is_Miaoli = fields.Boolean('苗栗縣')
    is_Nantou = fields.Boolean('南投縣')
    is_Yilan = fields.Boolean('宜蘭縣')
    is_Tainan = fields.Boolean('台南市')
    is_Kaohsiung = fields.Boolean('高雄市')
    is_Chiayi = fields.Boolean('嘉義市')
    is_Chiayi2 = fields.Boolean('嘉義縣')
    is_Pingtung = fields.Boolean('屏東縣')
    is_Taitung = fields.Boolean('臺東縣')
    is_Hualien = fields.Boolean('花蓮市')
    is_Penghu = fields.Boolean('澎湖縣')
    is_Kimen = fields.Boolean('金門縣')
    is_Nangan = fields.Boolean('連江縣')

    @api.onchange('is_Taiwan')
    def is_all_taiwan(self):
        if self.is_Taiwan is True:
           self.is_North = True
           self.is_Central = True
           self.is_South = True
           self.is_East = True
        else:
            self.is_North = False
            self.is_Central = False
            self.is_South = False
            self.is_East = False

    @api.onchange('is_North')
    def is_all_North(self):
        if self.is_North is True:
           self.is_Taipei = True
           self.is_Xinbei = True
           self.is_Taoyuan = True
           self.is_Hsinchu = True
           self.is_Hsinchu2 = True
           self.is_Keelung = True
        else:
           self.is_Taipei = False
           self.is_Xinbei = False
           self.is_Taoyuan = False
           self.is_Hsinchu = False
           self.is_Hsinchu2 = False
           self.is_Keelung = False

    @api.onchange('is_Central')
    def is_all_Central(self):
        if self.is_Central is True:
            self.is_Taichung = True
            self.is_Changhua = True
            self.is_Yunlin = True
            self.is_Miaoli = True
            self.is_Nantou = True
            self.is_Yilan = True
        else:
            self.is_Taichung = False
            self.is_Changhua = False
            self.is_Yunlin = False
            self.is_Miaoli = False
            self.is_Nantou = False
            self.is_Yilan = False

    @api.onchange('is_South')
    def is_all_South(self):
        if self.is_South is True:
            self.is_Tainan = True
            self.is_Kaohsiung = True
            self.is_Chiayi = True
            self.is_Chiayi2 = True
            self.is_Pingtung = True
        else:
            self.is_Tainan = False
            self.is_Kaohsiung = False
            self.is_Chiayi = False
            self.is_Chiayi2 = False
            self.is_Pingtung = False

    @api.onchange('is_East')
    def is_all_East(self):
        if self.is_East is True:
            self.is_Taitung = True
            self.is_Hualien = True
            self.is_Penghu = True
            self.is_Kimen = True
            self.is_Nangan = True
        else:
            self.is_Taitung = False
            self.is_Hualien = False
            self.is_Penghu = False
            self.is_Kimen = False
            self.is_Nangan =False

    def search_area_donor(self):
        number = 0
        action = self.env.ref('cdg_base.normal_p_action').read()[0]
        action['context'] = {}  # remove default domain condition in search box
        action['domain'] = []  # remove any value in search box

        action['domain'] = [('report_send', '=' , True),('postal_code_id.city', '=', u'台北市')]
        number = len(self.env['normal.p'].search([('report_send', '=' , True),('postal_code_id.city', '=', u'台北市')], order = "zip"))

        action['views'] = [
            [self.env.ref('cdg_base.normal_p_tree').id, 'tree'],
            [self.env.ref('cdg_base.normal_p_form').id, 'form'],
        ]
        action['limit'] = 1000
        return action
