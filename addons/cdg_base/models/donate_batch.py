# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DonateBatch(models.Model):
    _name = 'donate.batch'
    _rec_name = 'name'
    _description = u'批次捐款'

    name = fields.Char()
    donate_user = fields.Many2one(comodel_name='normal.p', string='捐款者')
    tag_bridge = fields.Boolean(string='造橋')
    tag_road = fields.Boolean(string='鋪路')
    tag_coffin = fields.Boolean(string='施棺')
    tag_food = fields.Boolean(string='伙食費')
    tag_allowance = fields.Boolean(string='窮困扶助')
    tag_other = fields.Boolean(string='其他工程')
    donate_price = fields.Integer(string='捐款金額')
    donate_total_price = fields.Integer(string='捐款總額', compute='compute_donate_total')
    donate_date = fields.Date(string='捐款日期', default=lambda self: fields.Date.today())
    donate_list = fields.One2many(string='捐款明細', comodel_name='donate.batch.line', inverse_name='parent_id')

    @api.depends('donate_list.donate_price')
    def compute_donate_total(self):
        for row in self:
            for line in row.donate_list:
                row.donate_total_price += line.donate_price

    def check_donate_type(self):
        member = self.env['normal.p'].search([('w_id', '=', self.donate_user.w_id)])
        if self.tag_bridge:
            self.set_donate_list(member, 1)
        if self.tag_road:
            self.set_donate_list(member, 2)
        if self.tag_coffin:
            self.set_donate_list(member, 3)
        if self.tag_food:
            self.set_donate_list(member, 4)
        if self.tag_allowance:
            self.set_donate_list(member, 5)
        if self.tag_other:
            self.set_donate_list(member, 6)
        self.tag_bridge = self.tag_road = self.tag_coffin = self.tag_food = self.tag_allowance = self.tag_other = False
        self.donate_price = 0
        self.name = self.donate_user.name + u'的批次捐款'

    def set_donate_list(self, member, type=0):
        for line in member:
            self.write({
                'donate_list':
                    [(0, 0, {
                        'donate_user': line.id,
                        'donate_price': self.donate_price,
                        'donate_type': type
                    })]
            })


class DonateBatchLine(models.Model):
    _name = 'donate.batch.line'
    _rec_name = 'name'
    _description = u'批次捐款明細'

    name = fields.Char()
    parent_id = fields.Many2one(comodel_name='donate.batch')
    donate_user = fields.Many2one(comodel_name='normal.p', string='捐款者')
    donate_user_id = fields.Char(string='團員編號', compute='compute_set_donate')
    donate_user_number = fields.Char(string='序號', compute='compute_set_donate')
    donate_type = fields.Selection(selection=[(1, '造橋'), (2, '補路'), (3, '施棺'), (4, '伙食費'), (5, '窮困扶助'), (6, '其他工程')],
                                   string='捐款種類', default=1, index=True)
    donate_price = fields.Integer(string='捐款金額')
    new_coding = fields.Char(string='新編捐款者編號', compute='compute_set_donate')

    @api.depends('donate_user')
    def compute_set_donate(self):
        for line in self:
            line.donate_user_id = line.donate_user.w_id
            line.donate_user_number = line.donate_user.number
            line.new_coding = line.donate_user.new_coding



