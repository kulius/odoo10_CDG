# -*- coding: utf-8 -*-
from odoo import models, fields, api

class peoplestatistics(models.TransientModel):
    _name = 'people.statistics'
    _description = u'系統資料統計表'

    donor_statistics = fields.Integer(string='捐款人數',readonly = True)
    base_member_statistics = fields.Integer(string='基本會員',readonly = True)
    donate_member_statistics = fields.Integer(string='贊助會員', readonly=True)
    member_total = fields.Integer(string='會員總數', readonly=True)
    consultant_statistics = fields.Integer(string='顧問', readonly=True)
    report_send = fields.Integer(string='寄送季報表', readonly=True)

    def count_people(self):
        self.donor_statistics = len(self.env['normal.p'].search([]))
        self.base_member_statistics = len(self.env['normal.p'].search([('type.id','=', 2 )]))
        self.donate_member_statistics = len(self.env['normal.p'].search([('type.id','=', 3 )]))
        self.member_total = self.base_member_statistics + self.donate_member_statistics
        self.consultant_statistics = len(self.env['normal.p'].search([('type.id','=', 4 )]))
        self.report_send = len(self.env['normal.p'].search([('report_send','=', True )]))