# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging, datetime
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ItemsDonate(models.Model):
    _name = 'items.donate'

    name = fields.Char('捐贈者')
    item_name = fields.Char('品名')
    addr = fields.Char('地址')
    phone = fields.Char('電話')
    money = fields.Integer('金額')
    items_id = fields.Char('品項編號', readonly=True)

    @api.model
    def create(self,vals):
        res_id = super(ItemsDonate, self).create(vals)
        res_id.items_id = self.env['ir.sequence'].next_by_code('items.donate')
        return res_id