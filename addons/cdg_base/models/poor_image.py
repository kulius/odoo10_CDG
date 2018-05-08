# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api

class PoorImage(models.Model):
    _name = 'poor.image'
    _order = "write_date asc"

    case_code = fields.Many2one(comodel_name='poor.base',string="案件")
    case_image = fields.Binary("案件照片資料")
    case_image_name = fields.Char('照片名稱')


