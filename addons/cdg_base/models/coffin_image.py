# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api

class CoffinImage(models.Model):
    _name = 'coffin.image'

    case_code = fields.Many2one(comodel_name='coffin.base',string="案件")
    case_image = fields.Binary("案件文件資料")
    case_image_name = fields.Char('文件名稱')