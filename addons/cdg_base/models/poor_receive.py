# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api

class PoorReceive(models.Model):
    _name = 'poor.receive'

    case_code = fields.Many2one(comodel_name='poor.base',string="案件")
    receive_date = fields.Date("領款時間")
    receive_money = fields.Integer('領款金額')


