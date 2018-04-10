# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ItemsDonate(models.Model):
    _name = 'items.name'

    name = fields.Char(string='品名')
