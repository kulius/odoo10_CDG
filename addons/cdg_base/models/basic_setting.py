# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api

class CWorker(models.Model):
    _name = 'basic.setting'

    Basic_donations = fields.Integer(string="基本捐助款", default=100)
    Annual_membership_fee = fields.Integer(string="會員年費", default=1200)
    Annual_consultants_fee = fields.Integer(string="顧問年費", default=10000)
    coffin_amount = fields.Integer(string="施棺滿足額", default=30000)

