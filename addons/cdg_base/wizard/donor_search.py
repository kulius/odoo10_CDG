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


    def search_area_donor(self):
     if self.is_Taiwan:

        ids = self.env['normal.p'].search([('postal_code_id','>=', 369),('postal_code_id','<=', 736),('report_send','=',True)],order="postal_code_id asc").ids



        docargs = {
            'docs': ids,
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'cdg_base.cashier_list.xlsx',
            'datas': docargs
        }
     else:
         raise ValidationError(u'全臺灣請打勾')
