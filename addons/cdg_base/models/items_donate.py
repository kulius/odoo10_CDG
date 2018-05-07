# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging, datetime
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ItemsDonate(models.Model):
    _name = 'items.donate'

    name = fields.Char('捐贈者')
    donate_date = fields.Date('捐助日期')
    item_name = fields.Char('品名')
    addr = fields.Char('地址')
    phone = fields.Char('電話')
    money = fields.Integer('金額')
    number = fields.Char('數量')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員',readonly = True)
    items_id = fields.Char('品項編號', readonly=True)
    tax_id_number = fields.Char('統一編號')
    invoice_number = fields.Char('發票號碼')
    print_state = fields.Boolean(string='列印狀態', default=False)


    @api.model
    def create(self,vals):
        res_id = super(ItemsDonate, self).create(vals)
        res_id.items_id = self.env['ir.sequence'].next_by_code('items.donate')
        res_id.key_in_user = self.env.uid
        return res_id

    def print_receipt(self):
        for line in self:
            if line.items_id and (line.tax_id_number or line.invoice_number):
                data = {
                    'ID':line.id,
                }
                return self.env['report'].get_action([], 'cdg_base.items_receipt_print', data)
            elif not line.items_id:
                raise ValidationError(u'請先存檔才能列印收據')
            elif not line.tax_id_number or not line.invoice_number:
                raise ValidationError(u'發票號碼或者統一編號未輸入，因此無法列印收據')