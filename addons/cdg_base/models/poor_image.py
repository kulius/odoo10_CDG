# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api

class PoorBase(models.Model):
    _name = 'poor.image'

    case_code = fields.Many2one(comodel_name='poor.base',string="案件")
    case_image = fields.Binary("案件影像資料")
    case_image_name = fields.Char('影像資料名稱')


