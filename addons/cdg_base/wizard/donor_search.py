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
    Taipei_Zhongzheng = fields.Boolean('中正區')
    Taipei_Datong = fields.Boolean('大同區')
    Taipei_Zhongshan = fields.Boolean('中山區')
    Taipei_Songshan = fields.Boolean('松山區')
    Taipei_Da_an = fields.Boolean('大安區')
    Taipei_Wanhua = fields.Boolean('萬華區')
    Taipei_Xinyi = fields.Boolean('信義區')
    Taipei_Shilin = fields.Boolean('士林區')
    Taipei_Beitou = fields.Boolean('北投區')
    Taipei_Neihu = fields.Boolean('內湖區')
    Taipei_Nangang = fields.Boolean('南港區')
    Taipei_Wenshan = fields.Boolean('文山區')

    is_Keelung = fields.Boolean('基隆市')
    Keelung_Ren_ai = fields.Boolean('仁愛區')
    Keelung_Xinyi = fields.Boolean('信義區')
    Keelung_Zhongzheng = fields.Boolean('中正區')
    Keelung_Zhongshan = fields.Boolean('中山區')
    Keelung_Anle = fields.Boolean('安樂區')
    Keelung_Nuannuan = fields.Boolean('暖暖區')
    Keelung_Qidu = fields.Boolean('七堵區')

    is_Xinbei = fields.Boolean('新北市')
    New_Taipei_Wanli = fields.Boolean('萬里區')
    New_Taipei_Jinshan = fields.Boolean('金山區')
    New_Taipei_Banqiao = fields.Boolean('板橋區')
    New_Taipei_Xizhi = fields.Boolean('汐止區')
    New_Taipei_Shenkeng = fields.Boolean('深坑區')
    New_Taipei_Shiding = fields.Boolean('石碇區')
    New_Taipei_Ruifang = fields.Boolean('瑞芳區')
    New_Taipei_Pingxi = fields.Boolean('平溪區')
    New_Taipei_Shuangxi = fields.Boolean('雙溪區')
    New_Taipei_Gongliao = fields.Boolean('貢寮區')
    New_Taipei_Xindian = fields.Boolean('新店區')
    New_Taipei_Pinglin = fields.Boolean('坪林區')
    New_Taipei_Wulai = fields.Boolean('烏來區')
    New_Taipei_Yonghe = fields.Boolean('永和區')
    New_Taipei_Zhonghe = fields.Boolean('中和區')
    New_Taipei_Tucheng = fields.Boolean('土城區')
    New_Taipei_Sanxia = fields.Boolean('三峽區')
    New_Taipei_Shulin = fields.Boolean('樹林區')
    New_Taipei_Yingge = fields.Boolean('鶯歌區')
    New_Taipei_Sanchong = fields.Boolean('三重區')
    New_Taipei_Xinzhuang = fields.Boolean('新莊區')
    New_Taipei_Taishan = fields.Boolean('泰山區')
    New_Taipei_Linkou = fields.Boolean('鶯歌區')
    New_Taipei_Luzhou = fields.Boolean('蘆洲區')
    New_Taipei_Wugu = fields.Boolean('五股區')
    New_Taipei_Bali = fields.Boolean('八里區')
    New_Taipei_Tamsui = fields.Boolean('淡水區')
    New_Taipei_Sanzhi = fields.Boolean('三芝區')
    New_Taipei_Shimen = fields.Boolean('石門區')



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
    Lienchiang_Nangan = fields.Boolean('南竿區')
    Lienchiang_Beigan = fields.Boolean('北竿區')
    Lienchiang_Juguang = fields.Boolean('莒光區')
    Lienchiang_Dongyin = fields.Boolean('東引區')

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

        return True
