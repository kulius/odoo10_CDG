# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api

class PoorDocument(models.Model):
    _name = 'poor.document'
    _order = "write_date asc"

    case_code = fields.Many2one(comodel_name='poor.base',string="案件")
    case_doc = fields.Binary("案件影像資料")
    case_doc_name = fields.Char('影像資料名稱')


