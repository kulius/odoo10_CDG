# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api

class workerdata(models.Model):
    _inherit = 'res.users'

    w_id = fields.Char(string='員工編號')
    name = fields.Char(string='姓名')
    con_phone = fields.Char(string='連絡電話(一)')
    con_phone2 = fields.Char(string='連絡電話(二)')
    cellphone = fields.Char(string='手機')
    email = fields.Char(string='Email')
    create_date1 = fields.Date(string='建檔日期')
    now_job = fields.Char(string='現在職稱')
    job_type = fields.Selection(selection=[(1, '一般員工'), (2, '收費員')], string='員工種類')

    self_iden = fields.Char(string='身分證字號')
    birth = fields.Date(string='出生日期')
    con_addr = fields.Char(string='通訊地址')
    sex = fields.Selection(selection=[('M', '男生'), ('F', '女生')], string='性別')
    come_date = fields.Date(string='到職日期')
    lev_date = fields.Date(string='離職日期')
    highest_stu = fields.Char(string='最高學歷')
    ps = fields.Text(string='備註')
    db_chang_date = fields.Date(string='異動日期')
    payment_method = fields.Integer('捐款方式')
    last_donate_date = fields.Date(string='上次輸入的捐款日期')

class workerdata_2(models.Model):
    _name = 'worker.data'

    w_id = fields.Char(string='員工編號')
    name = fields.Char(string='姓名')
    con_phone = fields.Char(string='連絡電話(一)')
    con_phone2 = fields.Char(string='連絡電話(二)')
    cellphone = fields.Char(string='手機')
    email = fields.Char(string='Email')
    create_date1 = fields.Date(string='建檔日期')
    now_job = fields.Char(string='現在職稱')
    job_type = fields.Selection(selection=[(1, '一般員工'), (2, '收費員')], string='員工種類')

    self_iden = fields.Char(string='身分證字號')
    birth = fields.Date(string='出生日期')
    con_addr = fields.Char(string='通訊地址')
    sex = fields.Selection(selection=[('M', '男生'), ('F', '女生')], string='性別')
    come_date = fields.Date(string='到職日期')
    lev_date = fields.Date(string='離職日期')
    highest_stu = fields.Char(string='最高學歷')
    ps = fields.Text(string='備註')
    db_chang_date = fields.Date(string='異動日期')