# -*- coding: utf-8 -*-
from odoo import models, fields, api

# 顧問 團員 會員 收費員


class PeopleType(models.Model):
    _name = 'people.type'

    name = fields.Char(string='人員種類')
    people_in = fields.Many2many(comodel_name='normal.p',string='人員有誰')
    len_people = fields.Integer(compute='count_people',string='人數',store=True)

    def count_people(self):
        for line in self:
            line.len_people = len(line.people_in)
