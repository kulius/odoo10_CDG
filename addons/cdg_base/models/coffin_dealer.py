# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import *

class CoffinBase(models.Model):
    _name = 'coffin.dealer'

    name = fields.Char('處理者姓名')