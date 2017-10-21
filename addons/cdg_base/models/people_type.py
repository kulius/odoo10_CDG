# -*- coding: utf-8 -*-
from odoo import models, fields, api

# 顧問 團員 會員 收費員


class PeopleType(models.Model):
    _name = 'people.type'

    name = fields.Char(string='人員種類')
    people_in = fields.One2many(comodel_name='normal.p',inverse_name='type',string='人員有誰')
