# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NewCoffin(models.TransientModel):
   _name = 'new.coffin'

   order_ids = fields.Many2many(comodel_name='donate.order', string='捐款明細')