# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AutoDonate(models.Model):
    _name = "auto.donateid"

    zip = fields.Char('郵政區號')
    area_number = fields.Integer('累積人數')