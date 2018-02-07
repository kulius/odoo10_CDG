# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class consultantjoinyear(models.Model):
    _name = 'consultant.join.year'

    year = fields.Integer(string='顧問聘僱年度查詢')

    def join_year_search(self):
        if self.year == 0 or self.year is False:
            raise ValidationError(u'請正確輸入繳費年度!')
        number = 0
        star_year = datetime.datetime.strptime(str(self.year + 1911) + '-01-01','%Y-%m-%d')
        end_year = datetime.datetime.strptime(str(self.year + 1911) + '-12-31', '%Y-%m-%d')
        star_time = star_year.strftime('%Y-%m-%d')
        end_time = end_year.strftime('%Y-%m-%d')
        action = self.env.ref('cdg_base.normal_p_action').read()[0]
        action['context'] = {}  # remove default domain condition in search box
        action['domain'] = []  # remove any value in search box
        action['domain'] = [('hire_date', '>=', star_time), ('hire_date', '<=', end_time)]
        number = len(self.env['normal.p'].search(
            [('type.id', '=', 4), ('hire_date', '>=', star_time), ('hire_date', '<=', end_time)]))
        action['views'] = [
            [self.env.ref('cdg_base.normal_p_tree').id, 'tree'],
            [self.env.ref('cdg_base.normal_p_form').id, 'form']
        ]
        action['limit'] = number
        return action