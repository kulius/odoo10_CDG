# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CashierBase(models.Model):
    _name = 'cashier.base'
    _description = u'收費員基本資料管理'

    c_id = fields.Char(string='收費員編號',readonly=1)
    name = fields.Char(string='收費員姓名')
    build_date = fields.Date(string='建檔日期')
    self_iden = fields.Char(string='身分證字號')
    con_phone = fields.Char(string='聯絡電話')
    con_phone2 = fields.Char(string='聯絡電話(二)')
    cellphone = fields.Char(string='手機')
    zip_code = fields.Char(string='通訊郵遞區號')
    con_addr = fields.Char(string='通訊地址')
    ps = fields.Text(string='備註')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員')
    temp_key_in_user = fields.Char(string='輸入人員')
    db_chang_date = fields.Date(string='異動日期')
    cashier = fields.Many2one(comodel_name='res.users', string="收費員登入")

    normal_cash = fields.Many2many(comodel_name='normal.p',string='捐款人繳費名冊')
    member_cash = fields.Many2many(comodel_name='normal.p',string='會員繳費名冊')
    consultant_cash = fields.Many2many(comodel_name='normal.p',string='顧問繳費名冊')

    @api.model
    def create(self,vals):
        res_id = super(CashierBase, self).create(vals)
        res_id.c_id = self.env['ir.sequence'].next_by_code('cashier.base')

        data=self.env['res.users'].create({
            'login': res_id.c_id,
            'password': "00000",
            'name': res_id.name,
            'sel_groups_16': 16,
        })

        res_id.write({
            'cashier': data.id
        })

        return res_id

    def donater_register(self):
        number = 0
        action = self.env.ref('cdg_base.normal_p_action').read()[0]
        action['context'] ={'search_default_top_of_home': 1} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        action['domain'] = [('cashier_name.id','=',self.id)]
        number = len(self.env['normal.p'].search([('cashier_name.id','=',self.id)]))
        action['limit'] = number
        return action

    def donater_donate_register(self):
        action = self.env.ref('cdg_base.action_wizard_cashier_block').read()[0]
        return action

    def member_register(self):
        number = 0
        action = self.env.ref('cdg_base.member_base_action').read()[0]
        action['context'] ={'search_default_top_of_home': 1} # remove default domain condition in search box
        action['domain'] =[] # remove any value in search box
        action['domain'] = [('member_id','!=',''),('cashier_name.id','=',self.id)]
        number = len(self.env['normal.p'].search([('cashier_name.id', '=', self.id)]))
        action['limit'] = number
        return action

    def consultant_register(self):
        number = 0
        action = self.env.ref('cdg_base.consultant_base_action').read()[0]
        action['context'] = {'search_default_top_of_home': 1}  # remove default domain condition in search box
        action['domain'] = []  # remove any value in search box
        action['domain'] = [('consultant_id','!=', ''),('cashier_name.id', '=', self.id)]
        number = len(self.env['normal.p'].search([('cashier_name.id', '=', self.id)]))
        action['limit'] = number
        return action

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if u'\u4e00' <= name <=u'\u9fff':
            domain = [('name', operator, name)]
        else:
            domain = [('c_id', operator, name)]

        banks = self.search(domain + args, limit=limit)
        return banks.name_get()

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "{%s} %s" % (record.c_id, record.name)
            result.append((record.id, name))
        return result
