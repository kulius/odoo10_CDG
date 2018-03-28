# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging, datetime
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class DonateSingle(models.Model):
    _name = 'old.donate.single'
    _rec_name = 'donate_id'
    _order = 'donate_date desc'
    _description = u'捐款作業管理'

    # name = fields.Many2one(comodel_name='normal.p',string='姓名')

    paid_id = fields.Char(string='收費編號', readonly=True)
    donate_id = fields.Char(string='收據編號', readonly=True)
    donate_member = fields.Many2one(comodel_name='normal.p', string='捐款者',
                                    states={2: [('readonly', True)]}, required=True)  # demo用
    w_id = fields.Char('舊團員編號', related='donate_member.w_id')  # 歷史捐款明細智慧按鈕需要用的, 拿掉就掛了
    new_coding = fields.Char('新捐款者編號', related='donate_member.new_coding')  # 歷史捐款明細智慧按鈕需要用的, 拿掉就掛了

    donate_member_w_id = fields.Char('舊團員編號', related='donate_member.w_id')  # search用   (轉檔時, 要把 related 去掉)
    donate_member_number = fields.Char('舊團員序號', related='donate_member.number')  # 轉檔時, 要把 related 去掉

    donate_member_new_coding = fields.Char('新捐款者編號', related='donate_member.new_coding')  # search用
    name = fields.Char(string='姓名', compute='set_donate_name', store=True)
    self_iden = fields.Char(string='身分證字號', compute='set_donate_name', store=True)
    cellphone = fields.Char(string='手機', compute='set_donate_name', store=True)
    con_phone = fields.Char(string='聯絡電話', compute='set_donate_name', store=True)
    zip_code = fields.Char(string='報表郵遞區號', compute='set_donate_name', store=True)
    con_addr = fields.Char(string='報表地址', compute='set_donate_name', store=True)
    zip = fields.Char(string='收據郵遞區號', compute='set_donate_name', store=True)
    rec_addr = fields.Char(string='收據地址', compute='set_donate_name', store=True)

    state = fields.Selection([(1, '已產生'), (2, '已列印'), (3, '已作廢')],
                             string='狀態', default=1, index=True)

    donate_total = fields.Integer(string='捐款總額', compute='compute_total', store=True)
    current_donate_total = fields.Integer('捐款總額小計')
    current_donate_people = fields.Integer('捐款人數小計')
    current_donate_project = fields.Integer('捐款項目小計')

    old_donate_total = fields.Integer(string='舊捐款總額')

    receipt_send = fields.Boolean(string='收據寄送')
    report_send = fields.Boolean(string='報表寄送')
    year_receipt_send = fields.Boolean(string='年收據寄送')
    bridge = fields.Boolean(string='造橋')
    road = fields.Boolean(string='補路')
    coffin = fields.Boolean(string='施棺')
    poor_help = fields.Boolean(string='貧困扶助')
    noassign = fields.Boolean(string='一般捐款')
    bridge_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    road_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    coffin_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    poor_help_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    noassign_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    payment_method = fields.Selection([(1, '現金'), (2, '郵政劃撥'), (3, '信用卡扣款'), (4, '銀行轉帳'), (5, '支票')], string='繳費方式',
                                      required=True)
    active = fields.Boolean(default=True)
    #    cash = fields.Boolean(string='現金', states={2: [('readonly', True)]})
    person_check = fields.Many2many(comodel_name="normal.p", string="捐款人名冊")
    family_check = fields.One2many(comodel_name='donate.family.line', inverse_name='parent_id', string='捐款人名冊',
                                   states={2: [('readonly', True)]})
    donate_list = fields.One2many(comodel_name='donate.order', inverse_name='donate_list_id', string='捐款明細',
                                  states={2: [('readonly', True)]})
    work_id = fields.Many2one(comodel_name='cashier.base', string='收費員', states={2: [('readonly', True)]},
                              required=True)
    temp_work_id = fields.Char(string='收費員')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', states={2: [('readonly', True)]},
                                  default=lambda self: self.env.uid)
    temp_key_in_user = fields.Char(string='輸入人員')

    print_user = fields.Many2one(comodel_name='res.users', string='列印人員', states={2: [('readonly', True)]})
    ps = fields.Text('備註')
    year_fee = fields.Boolean(string='年繳')

    history_donate_flag = fields.Boolean(string='是否上次捐款')
    #    history_payment_method = fields.Boolean('是否上次捐款方式')
    report_price_big = fields.Char(string='報表用大寫金額')
    report_donate = fields.Char(string='報表用捐款日期')
    donate_date = fields.Date('捐款日期')
    sreceipt_number = fields.Integer(string='收據筆數', compute='compute_total', store=True)
    print_count = fields.Integer(string='列印筆數', store=True)
    print_date = fields.Date('列印日期')
    donate_family_list = fields.Char('眷屬列表', compute='compute_family_list')
    print_all_donor_list = fields.Boolean(string='列印願意捐助的眷屬')

    clear_all_is_donate = fields.Boolean(string='清除 [是否捐助]')
    clear_all_is_merge = fields.Boolean(string='清除 [是否合併收據]')
    set_today = fields.Boolean(string='今天')

    last_donate_date = fields.Date('上次捐款日期')
    last_donate_type = fields.Selection(selection=[(01, '造橋'), (02, '補路'), (03, '施棺'), (05, '貧困扶助'), (06, '一般捐款')],
                                        string='捐款種類')
    cashier_name = fields.Char(string='normal_p的收費員')
    donor_show = fields.Boolean(string='只顯示捐款眷屬', default=True)