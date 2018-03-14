# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from passlib.context import CryptContext

import datetime

class CashierBlock(models.Model):
    _name = 'change.password'
    current_password = fields.Char('目前密碼')
    new_password = fields.Char('新密碼')




    def change_password(self):

        crypt_context = CryptContext(['pbkdf2_sha512', 'md5_crypt'], deprecated=['md5_crypt'])

        self.env['res.users'].search([('id', '=', self.env.uid)]).password_crypt = crypt_context.encrypt(self.new_password)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

