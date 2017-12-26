# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CoffinDonation(models.Model):
    _name = 'coffin.donation'

    name = fields.Char()
    new_coffin_ic = fields.Char(string='新施棺編號編號')
    new_donate_id = fields.Char(string='新捐款編號')
    coffin_id = fields.Char(string='施棺編號')
    donate_id = fields.Char(string='捐款編號', compute='set_donate_name', store=True)
    donate_price = fields.Char(string='捐款金額', compute='set_donate_name', store=True)
    coffin_donation_id = fields.Many2one(comodel_name='coffin.base')
    get_coffin_donate = fields.Many2one(comodel_name='donate.single', string='捐款者',domain=[('donate_id', '!=', ''), ('coffin', '=', True), ('state', '=', 1),('donate_total', '!=', '')])

    @api.depends('get_coffin_donate')
    def set_donate_name(self):
        for line in self:
            normal_p = line.get_coffin_donate
            line.donate_id = normal_p.donate_id
            line.donate_price = normal_p.donate_total
            line.coffin_id = self.coffin_donation_id.coffin_id

    def data_input_from_database(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 施棺捐款檔')
        for line in lines:
            id_create = self.create({
                'coffin_id': line[u'施棺編號'],
                'donate_id':line[u'捐款編號'],
                'donate_price':line[u'捐款金額'],
            })