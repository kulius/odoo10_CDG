# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PoorBase(models.Model):
    _name = 'poor.base'

    poor_id = fields.Char('專案編號')