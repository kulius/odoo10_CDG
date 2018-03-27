# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import *
import logging

# 一般人基本檔 團員 會員 收費員 顧問
_logger = logging.getLogger(__name__)

class BridgeData(models.Model):
    _name = 'bridge.data'

    bridge_code = fields.Char('橋樑編號', readonly=True)
    name = fields.Char('橋樑名稱')
    length = fields.Float('長度')
    width = fields.Float('寬度')
    height = fields.Float('高度')
    bridge_addr = fields.Char('橋樑地址')
    donate_date_start = fields.Date('募捐起日')
    donate_date_end = fields.Date('募捐迄日')
    build_date = fields.Date('建造日期')
    completed_date = fields.Date('完工日期')
    db_change_date = fields.Date('異動日期')
    numbers = fields.Integer('數字')

    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', ondelete='cascade')
    temp_key_in_user = fields.Char('輸入人員')

    @api.model
    def create(self, vals):
        res_id = super(BridgeData, self).create(vals)

        if res_id.name is False:
            raise ValidationError(u'橋樑名稱不得為空')

        res_id.bridge_code = self.env['ir.sequence'].next_by_code('bridge.data')
        res_id.key_in_user = self.env.uid
        return res_id

