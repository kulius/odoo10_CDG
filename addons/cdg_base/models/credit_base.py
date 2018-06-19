# -*- coding:utf-* -*-
from odoo import api,models,fields

class CreditBase(models.Model):
    _name = 'credit.base'
    name = fields.Char(related='credit_donate_name.name',store=True)

    credit_id = fields.Char('信用卡編號')
    credit_donate_name = fields.Many2one(comodel_name='normal.p', string='信用卡捐款人')
    credit_phone = fields.Char('手機')
    credit_owner_code = fields.Many2one(comodel_name='normal.p', string='信用卡持卡人')
    credit_parent = fields.Many2one(comodel_name='credit.base',string='信用卡戶長')
    credit_list = fields.One2many(comodel_name='credit.base', inverse_name='credit_parent', string='信用卡捐款名單')

    credit_zip = fields.Char('信用卡郵遞區號')
    credit_addr = fields.Char('信用卡收據地址')
    is_sent = fields.Boolean('每次寄送')
    year_sent = fields.Boolean('年底一次開立')
    no_need = fields.Boolean('不需收據')
    debit_method = fields.Selection(selection=[(1, '5日扣款'), (2, '20日扣款'), (3, '季日扣款'), (4, '年繳扣款'), (5, '單次扣款')],string='信用卡扣款方式')
    bridge_money = fields.Integer('信用卡造橋金額')
    road_money = fields.Integer('信用卡補路金額')
    coffin_money = fields.Integer('信用卡施棺金額')
    poor_money = fields.Integer('信用卡貧困扶助金額')
    normal_money = fields.Integer('信用卡一般捐款金額')
    credit_money = fields.Integer('扣款總額')

    donate_batch_setting = fields.Boolean(string='確認捐款', default=False)

    # credit_number = fields.Char('信用卡卡號')

    @api.model
    def create(self, vals):
        res_id = super(CreditBase, self).create(vals)
        res_id.credit_id = self.env['ir.sequence'].next_by_code('credit.base')
        return res_id

    def credit_batch(self, ids):
        res = []
        for line in ids:
            res.append([4, line])
        wizard_data = self.env['wizard.credit.batch'].create({
            'donate_line': res
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.credit.batch',
            'name': '信用卡批次項目',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    @api.onchange('credit_owner_code')
    def set_credit_data(self):
        data = self.env['normal.p'].search([('id','=',self.credit_owner_code.ids)])
        if self.credit_owner_code != False:
            self.credit_phone = data.cellphone
            self.credit_zip = data.credit_zip
            self.credit_addr = data.credit_addr
            self.debit_method = data.debit_method
            self.is_sent = data.is_sent
            self.year_sent = data.year_sent
            self.no_need = data.no_need

    @api.onchange('credit_owner_code')
    def set_credit_parent(self):
        if self.credit_owner_code == self.credit_donate_name:
            self.credit_parent = self.env['credit.base'].search([('credit_owner_code','=',self.credit_owner_code.id)])


    @api.onchange('bridge_money','road_money','coffin_money','poor_money','normal_money')
    def compute_donate_total(self):
        self.credit_money = 0
        self.credit_money = self.bridge_money + self.road_money + self.coffin_money + self.poor_money + self.normal_money

    def check_batch_donate(self):
        if self.donate_batch_setting == True:
            self.donate_batch_setting = False
        elif self.donate_batch_setting == False:
            self.donate_batch_setting = True
        return True
