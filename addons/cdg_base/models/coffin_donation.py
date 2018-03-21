# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CoffinDonation(models.Model):
    _name = 'coffin.donation'

    name = fields.Char(string='捐款者姓名', related='donate_order_id.donate_member.name')
    donate = fields.Integer(string='施棺捐款金額', related='donate_order_id.donate')
    donate_price = fields.Integer(string='施棺捐款金額(已用)', related='donate_order_id.used_money')
    use_amount = fields.Boolean(string='施棺捐款是否已支用', related='donate_order_id.use_amount')
    available_balance = fields.Integer(string='可用餘額', related='donate_order_id.available_balance')

    coffin_donation_id = fields.Many2one(comodel_name='coffin.base')
    old_coffin_donation_id = fields.Many2one(comodel_name='coffin.base')
    donate_single_id = fields.Many2one(comodel_name='donate.single', string='捐款編號')
    donate_order_id = fields.Many2one(comodel_name='donate.order', string='捐款者 (可用餘額)' , domain=[('donate_type', '=', 3),('available_balance', '!=', 0)])
    donate_id =  fields.Char(string='捐款編號', related='donate_order_id.donate_id')

    @api.onchange('donate_order_id')
    def set_used_money(self):
        self.donate_price = self.donate
        self.donate = 0
        self.available_balance = 0
        self.use_amount = True

    def data_input_from_database(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 施棺捐款檔')
        for line in lines:
            id_create = self.create({
                'coffin_id': line[u'施棺編號'],
                'donate_id':line[u'捐款編號'],
                'donate_price':line[u'捐款金額'],
            })