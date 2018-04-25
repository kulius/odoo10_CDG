# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo import models, fields, api

class PoorBase(models.Model):
    _name = 'poor.base'

    #純文字的欄位
    name = fields.Char('案主姓名')
    self_iden = fields.Char('案主身分證號')
    birth = fields.Date('案主出生年月日')
    case_id = fields.Char('案件編號')
    telephone = fields.Char('案主電話')
    phone = fields.Char('案主手機')
    relationship = fields.Char('聯絡人/關係')
    relate_phone = fields.Char('聯絡人電話')
    apply_method = fields.Text('申請管道')
    rec_int = fields.Text('資源整合查詢')
    Process_status = fields.Text('處理狀況')
    check_date = fields.Date('核發日期')
    visit_completed_date = fields.Date('訪視完成日期')
    pick_up_date = fields.Date('領件日期')
    apply_date = fields.Date('申請日期')
    visit_member = fields.Text('訪視志工人員')
    # 上傳案件照片
    rec_zip = fields.Char(string='戶籍郵政區號')
    rec_addr = fields.Char(string='戶籍地址')
    mail_zip = fields.Char(string='通訊郵遞區號')
    mail_addr = fields.Char(string='通訊地址')
    IsApproved = fields.Boolean('是否核准')

    case_process = fields.Selection([(1, '訪視完成'), (2, '報告已送')], '案件進度')
    reward_method = fields.Selection([(1,'現金'),(2,'匯款')],'領款方式')

    #救助情形
    month = fields.Selection([(1, '1個月'), (2, '2個月'),(3, '3個月'),(4, '4個月'),(5, '5個月'),(6, '6個月')], '提領月數')
    allow_money = fields.Integer('申請總額')
    once_money = fields.Integer('單次金額')
    receive_money = fields.Integer('已領金額')
  #  poor_receive_time = fields.One2many()




    @api.model
    def create(self, vals):
        res_id = super(PoorBase, self).create(vals)

        if res_id.name is False or res_id.self_iden is False:
            raise ValidationError('姓名或身分證號不能為空白')
        else:
            res_id.case_id = res_id.case_date[0:4] + res_id.case_date.split('-')[1]

        return res_id

