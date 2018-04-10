# -*- coding: utf-8 -*-
from odoo import models, fields, api

class changestate(models.Model):
    _name = 'change.state'
    _description = u'批次變更列印狀態'

    star_donate_id = fields.Char(string='收據編號-起')
    end_donate_id = fields.Char(string='收據編號-訖')
    change_user = fields.Many2one(comodel_name='res.users', string='變更人員', default=lambda self: self.env.uid)
    key_in_user = fields.Many2one(comodel_name='res.users', string='建檔人員')
    cashier_code = fields.Many2one(comodel_name='cashier.base', string='收費員')

    def change_state(self):
        datas = self.env['donate.single'].search([('donate_id','>=',self.star_donate_id),('donate_id','<=',self.end_donate_id),('key_in_user','=',self.key_in_user.id),('work_id','=',self.cashier_code.id)])
        for line in datas:
            if line.state == 2:
                line.state = 1
        return True