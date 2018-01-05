# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class DonateOrder(models.Model):
    _name = 'donate.order'

    # name = fields.Many2one(comodel_name='normal.p',string='姓名')
    donate_list_id = fields.Many2one(comodel_name='donate.single')
    con_phone = fields.Char(string='連絡電話')
    p_type = fields.Char(string='人員種類')
    donate = fields.Integer(string='捐款金額')
    donate_total = fields.Integer(string='捐款總額')
    donate_type = fields.Selection(selection=[(01, '造橋'), (02, '補路'), (03, '施棺'), (04, '伙食費'), (05, '貧困扶助'),(06, '不指定'), (99, '其他工程')],
                                   string='捐款種類')
    state = fields.Selection([(1, '已產生'), (2, '已作廢')],
                             string='狀態', default=1, index=True)
    donate_member = fields.Many2one(comodel_name='normal.p', string='捐款人姓名')
    paid_id = fields.Char(string='收費編號')
    donate_id = fields.Char(string='捐款編號')
    donate_w_id = fields.Char(string='團員編號')
    donate_w_id_number = fields.Char(string='序號')
    donate_date = fields.Date(string='捐款日期')
    self_id = fields.Char(string='身分證字號')
    clerk = fields.Char(string='收費員編號')
    key_in_user = fields.Many2one(comodel_name='c.worker', string='輸入人員')
    temp_key_in_user = fields.Char(string='輸入人員')
    db_key_in_user = fields.Char(string='資料庫紀錄輸入人員')
    report_year = fields.Boolean(string='收據年度開立')
    db_chang_date = fields.Date(string='異動日期')
    receipt_send = fields.Boolean(string='收據寄送')
    report_send = fields.Boolean(string='報表寄送')
    year_receipt_send = fields.Boolean(string='年收據寄送')
    bridge = fields.Boolean(string='造橋')
    road = fields.Boolean(string='補路')
    coffin = fields.Boolean(string='施棺')
    poor_help = fields.Boolean(string='貧困扶助')
    others = fields.Boolean(string='不指定')
    bridge_money = fields.Integer(string='$')
    road_money = fields.Integer(string='$')
    coffin_money = fields.Integer(string='$')
    poor_help_money = fields.Integer(string='$')
    others_money = fields.Integer(string='$')
    payment_method = fields.Integer(string='捐款方式')
    cash = fields.Boolean(string='現金')
    mail = fields.Boolean(string='郵政劃撥')
    credit_card = fields.Boolean(string='信用卡扣款')
    bank = fields.Boolean(string='銀行轉帳')

    address = fields.Char(string='住址')
    city = fields.Char(string='市區')

    use_amount = fields.Boolean(string='施棺捐款是否已支用', default=False)

    report_big = fields.Char()
    report_price = fields.Integer()

    # @api.onchange('name')
    # def setconphone(self):
    #     self.con_phone = self.name.con_phone
    #     self.p_type = self.name.type.name
    #     self.donate_w_id = self.name.w_id.id

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.donate_id
            result.append((record.id, name))
        return result

    def data_input_from_database(self):
        data = self.env['base.external.dbsource'].search([])
        lines = data.execute('SELECT * FROM 捐款檔')
        i = 1
        for line in lines:
            _logger.error(' %s / %s', i, len(lines))
            user = self.env['normal.p'].search([('w_id', '=', line[u'團員編號']), ('number', '=', line[u'序號'])])
            if user.id > 0:
                self.create({
                    'paid_id': line[u'收費編號'],
                    'donate_id': line[u'捐款編號'],
                    'donate_w_id': line[u'團員編號'],
                    'donate_w_id_number': line[u'序號'],
                    'donate_member': user.id,
                    'donate_total': line[u'捐款總額'],
                    'donate_date': line[u'捐款日期'],
                    'donate': line[u'捐款金額'],
                    'donate_type': self.check_habbit(line[u'捐助種類編號']),
                    'clerk': line[u'收費員編號'],
                    'key_in_user': self.check_user(line[u'輸入人員']),
                    'db_chang_date': self.check(line[u'異動日期']),
                    'report_year': self.checkbool(line[u'收據年度開立'])
                })
            i += 1
    def cancel_donate(self):
        if self.state == 2:
            raise ValidationError(u'本捐款單已作廢!!')
        self.state = 2


    def checkbool(self, bool):
        if bool == 'Y':
            return True
        elif bool == 'N':
            return False

    def check(self, date_check):
        if date_check:
            return date_check
        else:
            return None

    def check_user(self, row):
        check = self.env['c.worker'].search([('w_id', '=', row)])
        if check.id > 0:
            return check.id
        else:
            return False

    def check_habbit(self, habbit=None):
        if habbit == u'01':
            return 01
        elif habbit == u'02':
            return 02
        elif habbit == u'03':
            return 03
        elif habbit == u'04':
            return 04
        elif habbit == u'05':
            return 05
        elif habbit == u'06':
            return 06
        elif habbit == u'99':
            return 99
        else:
            return None
