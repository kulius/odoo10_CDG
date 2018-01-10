# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CashierBase(models.Model):
    _name = 'cashier.base'

    c_id = fields.Char(string='收費員編號')
    name = fields.Char(string='收費員姓名')
    build_date = fields.Date(string='建檔日期')

    self_iden = fields.Char(string='身分證字號')
    con_phone = fields.Char(string='聯絡電話(一)')
    con_phone2 = fields.Char(string='聯絡電話(二)')
    cellphone = fields.Char(string='手機')
    zip_code = fields.Char(string='郵遞區號')
    con_addr = fields.Char(string='通訊地址')
    ps = fields.Text(string='備註')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員')
    temp_key_in_user = fields.Char(string='輸入人員')
    db_chang_date = fields.Date(string='異動日期')

    normal_cash = fields.Many2many(comodel_name='normal.p',string='捐款人繳費名冊')
    member_cash = fields.Many2many(comodel_name='normal.p',string='會員繳費名冊')
    consultant_cash = fields.Many2many(comodel_name='normal.p',string='顧問繳費名冊')

    def donater_register(self):
        action = self.env.ref('cdg_base.normal_p_action').read()[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        action['domain'] = ['&',('member_id','=',None),('consultant_id','=', None),('cashier_name','=',self.name)]
        return action

    def member_register(self):
        action = self.env.ref('cdg_base.member_base_action').read()[0]
        action['context'] ={} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        action['domain'] = [('member_id','!=',''),('cashier_name','=',self.name)]
        return action

    def consultant_register(self):
        action = self.env.ref('cdg_base.consultant_base_action').read()[0]
        action['context'] = {}  # remove default domain condition in search box
        action['domain'] = []  # remove any value in search box
        action['domain'] = [('consultant_id','!=', ''),('cashier_name', '=', self.name)]
        return action
