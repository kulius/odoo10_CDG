# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class DonateSingle(models.Model):
    _name = 'donate.single'

   #name = fields.Many2one(comodel_name='normal.p',string='姓名')

    paid_id = fields.Char(string='收費編號', readonly=True)
    donate_id = fields.Char(string='捐款編號', readonly=True)
    donate_member = fields.Many2one(comodel_name='normal.p', string='捐款者編號', domain=[('w_id','!=','')])# demo用
    name = fields.Char(string='姓名', compute='set_donate_name')
    self_iden = fields.Char(string='身分證字號', compute='set_donate_name', store=True)
    cellphone = fields.Char(string='手機', compute='set_donate_name', store=True)
    con_phone = fields.Char(string='連絡電話', compute='set_donate_name', store=True)
    zip_code = fields.Char(string='郵遞區號', compute='set_donate_name', store=True)
    con_addr = fields.Char(string='聯絡地址', compute='set_donate_name', store=True)

    donate_total = fields.Integer(string='捐款總額', compute='compute_total')

    receipt_send = fields.Boolean(string='收據寄送')
    report_send = fields.Boolean(string='報表寄送')
    year_receipt_send = fields.Boolean(string='年收據寄送')
    bridge = fields.Boolean(string='造橋')
    road = fields.Boolean(string='補路')
    coffin = fields.Boolean(string='施棺')
    poor_help = fields.Boolean(string='貧困扶助')
    bridge_money = fields.Integer(string='$')
    road_money = fields.Integer(string='$')
    coffin_money = fields.Integer(string='$')
    poor_help_money = fields.Integer(string='$')
    cash = fields.Boolean(string='現金')
    mail = fields.Boolean(string='郵政劃撥')
    credit_card = fields.Boolean(string='信用卡扣款')
    bank = fields.Boolean(string='銀行轉帳')

    donate_list = fields.One2many(comodel_name='donate.single.line', inverse_name='parent_id', string='捐款明細')

    @api.model
    def create(self, vals):
        res_id = super(DonateSingle, self).create(vals)
        max = self.env['donate.order'].search([], order='paid_id desc', limit=1)
        donate_id = max.donate_id
        int_max = int(donate_id[1:])+1
        res_id.write({
            'donate_id': 'A' + str(int_max)
        })
        res_id.add_to_list()
        return res_id

    @api.depends('donate_list')
    def compute_total(self):
        for line in self:
            for row in line.donate_list:
                line.donate_total += row.donate_price


    def add_to_list(self):
        max = self.env['donate.order'].search([], order='paid_id desc', limit=1)
        max_int = int(max.paid_id)+1
        if self.bridge:
            self.write({
                'donate_list':[(0, 0, {
                    'donate_id': self.donate_id,
                    'paid_id': str(max_int),
                    'donate_member': self.donate_member.id,
                    'donate_type': 1,
                    'donate_price': self.bridge_money
                })]
            })
            max_int = max_int + 1
        if self.road:
            self.write({
                'donate_list': [(0, 0, {
                    'donate_id': self.donate_id,
                    'paid_id': str(max_int),
                    'donate_member': self.donate_member.id,
                    'donate_type': 2,
                    'donate_price': self.road_money
                })]
            })
            max_int = max_int + 1
        if self.coffin:
            self.write({
                'donate_list': [(0, 0, {
                    'donate_id': self.donate_id,
                    'paid_id': str(max_int),
                    'donate_member': self.donate_member.id,
                    'donate_type': 3,
                    'donate_price': self.coffin_money
                })]
            })
            max_int = max_int + 1
        if self.poor_help:
            self.write({
                'donate_list': [(0, 0, {
                    'donate_id': self.donate_id,
                    'paid_id': str(max_int),
                    'donate_member': self.donate_member.id,
                    'donate_type': 4,
                    'donate_price': self.poor_help_money
                })]
            })
            max_int = max_int + 1





    @api.depends('donate_member')
    def set_donate_name(self):
        for line in self:
            normal_p = line.donate_member
            line.name = normal_p.name
            line.cellpnone = normal_p.cellphone
            line.con_phone = normal_p.con_phone
            line.self_iden = normal_p.self_iden
            line.zip_code = normal_p.zip_code
            line.con_addr = normal_p.con_addr


class DonateSingleLine(models.Model):
    _name = 'donate.single.line'

    parent_id = fields.Many2one(comodel_name='donate.single')
    donate_id = fields.Char(string='捐款編號', readonly=True)
    paid_id = fields.Char(string='收費編號', readonly=True)
    donate_member = fields.Many2one(comodel_name='normal.p', string='捐款人')
    donate_type = fields.Selection(selection=[(1, '造橋'), (2, '補路'), (3, '施棺'), (4, '伙食費'), (5, '窮困扶助'), (6, '其他工程')],
                                   string='捐款種類')
    donate_price = fields.Integer(string='捐款金額')

