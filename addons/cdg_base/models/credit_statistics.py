# -*- coding: utf-8 -*-
from odoo import models, fields, api

class creditstatistics(models.TransientModel):
    _name = 'credit.statistics'
    _description = u'信用卡資料統計表'

    credit_statistics = fields.Integer(string='信用卡捐款人數',readonly = True)
    five_debit = fields.Integer(string='五日扣款人數', readonly=True)
    twenty_debit = fields.Integer(string='二十日扣款人數', readonly=True)
    season_debit = fields.Integer(string='季扣款人數', readonly=True)
    year_debit = fields.Integer(string='年扣款人數', readonly=True)
    once_debit = fields.Integer(string='單次扣款人數', readonly=True)

    def count_people(self):
        self.credit_statistics = len(self.env['normal.p'].search([('debit_method','!=',False),('is_donate','=',True)]))
        self.five_debit = len(self.env['normal.p'].search([('debit_method','=',1),('is_donate','=',True)]))
        self.twenty_debit = len(self.env['normal.p'].search([('debit_method', '=', 2),('is_donate','=',True)]))
        self.season_debit = len(self.env['normal.p'].search([('debit_method', '=', 3),('is_donate','=',True)]))
        self.year_debit = len(self.env['normal.p'].search([('debit_method', '=', 4),('is_donate','=',True)]))
        self.once_debit = len(self.env['normal.p'].search([('debit_method', '=', 5),('is_donate','=',True)]))