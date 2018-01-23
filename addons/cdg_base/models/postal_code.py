# -*- coding: utf-8 -*-
from odoo import models, fields, api

class postal_code(models.Model):
    _name = 'postal.code'

    city = fields.Char(string='縣市')
    area = fields.Char(string='行政區')
    zip = fields.Char(string='郵遞區號')