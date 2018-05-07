# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ItemsNumber(models.Model):
    _name = 'items.number'

    number = fields.Integer()
