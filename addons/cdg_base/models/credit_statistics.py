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
    five_debit_money = fields.Integer(string='五日扣款金額', readonly=True)
    twenty_debit_money = fields.Integer(string='二十日扣款金額', readonly=True)
    season_debit_money = fields.Integer(string='季扣款金額', readonly=True)
    year_debit_money = fields.Integer(string='年扣款金額', readonly=True)
    once_debit_money = fields.Integer(string='單次扣款金額', readonly=True)

    def count_people(self):
        self.credit_statistics = len(self.env['normal.p'].search([('debit_method','!=',False),('is_donate','=',True)]))
        self.five_debit = len(self.env['normal.p'].search([('debit_method','=',1),('is_donate','=',True)]))
        self.twenty_debit = len(self.env['normal.p'].search([('debit_method', '=', 2),('is_donate','=',True)]))
        self.season_debit = len(self.env['normal.p'].search([('debit_method', '=', 3),('is_donate','=',True)]))
        self.year_debit = len(self.env['normal.p'].search([('debit_method', '=', 4),('is_donate','=',True)]))
        self.once_debit = len(self.env['normal.p'].search([('debit_method', '=', 5),('is_donate','=',True)]))

        self.five_debit_money = 0
        self.twenty_debit_money = 0
        self.year_debit_money = 0
        self.once_debit_money = 0
        self.season_debit_money = 0



        data1 = self.env['normal.p'].search([('debit_method','=',1),('credit_family','!=',False)])
        for data in data1:
            for line in data.credit_family:
                if line.credit_is_donate == True:
                    self.five_debit_money += line.credit_total_money

        data2 = self.env['normal.p'].search([('debit_method', '=', 2),('credit_family','!=',False)])
        for data in data2:
            for line in data.credit_family:
                if line.credit_is_donate == True:
                    self.twenty_debit_money += line.credit_total_money

        data3 = self.env['normal.p'].search([('debit_method', '=', 3),('credit_family','!=',False)])
        for data in data3:
            for line in data.credit_family:
                if line.credit_is_donate == True:
                    self.season_debit_money += line.credit_total_money

        data4 = self.env['normal.p'].search([('debit_method', '=', 4),('credit_family','!=',False)])
        for data in data4.credit_family:
            for line in data:
                if line.credit_is_donate == True:
                    self.year_debit_money += line.credit_total_money

        data5 = self.env['normal.p'].search([('debit_method', '=', 5),('credit_family','!=',False)])
        for data in data5:
            for line in data.credit_family:
                if line.credit_is_donate == True:
                    self.once_debit_money += line.credit_total_money