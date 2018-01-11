# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CoffinDonation(models.Model):
    _name = 'coffin.donation'

    name = fields.Char(string='捐款者姓名', related='donate_order_id.donate_member.name')
    donate_price = fields.Integer(string='施棺捐款金額', related='donate_order_id.donate')

    coffin_donation_id = fields.Many2one(comodel_name='coffin.base')
    old_coffin_donation_id = fields.Many2one(comodel_name='coffin.base')
    donate_single_id = fields.Many2one(comodel_name='donate.single', string='捐款編號')
    donate_order_id = fields.Many2one(comodel_name='donate.order', string='捐款者 (金額)' , domain=['|',('donate_type', '=', 3),('donate_type', '=', 6),('available_balance', '!=', 0)])

    def data_input_from_database(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 施棺捐款檔')
        for line in lines:
            id_create = self.create({
                'coffin_id': line[u'施棺編號'],
                'donate_id':line[u'捐款編號'],
                'donate_price':line[u'捐款金額'],
            })