# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class donatetotalinquire(models.Model):
    _name = 'donate.total.inquire'
    _description = u'捐款總額查詢'

    star_year = fields.Char(string='捐款日期(民國年)-起')
    end_year = fields.Char(string='捐款日期(民國年)-訖')
    donate_total = fields.Integer(string='查詢金額')

    def inquire_donate_total(self):
        star_time = datetime.datetime.strptime(str(str(int(self.star_year) + 1911)+'-01-01'), '%Y-%m-%d').strftime('%Y-%m-%d')
        end_time = datetime.datetime.strptime(str(str(int(self.end_year) + 1911)+'-12-31'), '%Y-%m-%d').strftime('%Y-%m-%d')
        data = self.env['donate.single'].search([('donate_date', '>=', star_time), ('donate_date', '<=', end_time),('donate_total', '>=', self.donate_total)],order='donate_date asc').ids

        docargs = {
            'docs': data,
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'cdg_base.donate_totally.xlsx',
            'datas': docargs
        }