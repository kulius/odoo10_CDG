# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging, time
from datetime import datetime

class MemberUndonate(models.Model):
    _name = "member.undonate"

    donated_year = fields.Char('已繳費年度')
    undonated_year = fields.Char('未繳費年度')



    def excel(self):

        donated_data = list()
        undonated_data = list()
        data = list()


        donated_id = self.env['associatemember.fee'].search([('year','=',self.donated_year),('fee_date','!=',False)])
        for line in donated_id:
            donated_data.append(line.normal_p_id.id)



        undonate_id = self.env['associatemember.fee'].search([('year','=',self.undonated_year),('fee_date','=',False)])
        for line in undonate_id:
            undonated_data.append(line.normal_p_id.id)


        repeat_data = list(set(donated_data) & set(undonated_data))



        docargs = {
            'docs': repeat_data,
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'cdg_base.member_undonate_list.xlsx',
            'datas': docargs
        }

