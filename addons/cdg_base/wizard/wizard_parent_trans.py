# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WizardCashierDonor(models.TransientModel):
    _name = 'wizard.parent.trans'

    normal_p_code = fields.Many2one(comodel_name='normal.p', string='捐款者')

    def set_parent(self):

        data = self.env['normal.p'].search([('new_coding','=',self.normal_p_code.new_coding)])

        for line in data.donate_family1:
            line.parent = self.normal_p_code.parent





