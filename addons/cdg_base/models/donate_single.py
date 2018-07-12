# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging, datetime
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class DonateSingle(models.Model):
    _name = 'donate.single'
    _rec_name = 'donate_id'
    _order = 'donate_id'
    _description = u'捐款作業管理'

    # name = fields.Many2one(comodel_name='normal.p',string='姓名')

    paid_id = fields.Char(string='收費編號', readonly=True)
    donate_id = fields.Char(string='收據編號', readonly=True)
    donate_member = fields.Many2one(comodel_name='normal.p', string='捐款者',
                                    required = True, index = True)  # demo用  轉檔時, 要把required = True 拿掉
    w_id = fields.Char('舊團員編號', related='donate_member.w_id')  # 歷史捐款明細智慧按鈕需要用的, 拿掉就掛了
    new_coding = fields.Char('新捐款者編號', related='donate_member.new_coding')  # 歷史捐款明細智慧按鈕需要用的, 拿掉就掛
    donate_member_w_id = fields.Char('舊團員編號',related='donate_member.w_id') # search用   (轉檔時, 要把 related 去掉)
    donate_member_number = fields.Char('舊團員序號',related='donate_member.number') # 轉檔時, 要把 related 去掉
    # credit_parent = fields.Char('信用卡持卡人',related='donate_member.credit_parent.name')

    donate_member_new_coding = fields.Char('新捐款者編號',related='donate_member.new_coding')  # search用
    name = fields.Char(string='姓名',store=True)
    self_iden = fields.Char(string='身分證字號', compute='set_donate_name', store=True)
    cellphone = fields.Char(string='手機',  store=True)
    con_phone = fields.Char(string='聯絡電話',  store=True)
    zip_code = fields.Char(string='報表郵遞區號',  store=True)
    con_addr = fields.Char(string='報表地址',  store=True)
    zip = fields.Char(string='收據郵遞區號',  store=True)
    rec_addr = fields.Char(string='收據地址', store=True)

    state = fields.Selection(selection = [(1, '已產生'), (2, '已列印'), (3, '已作廢')], string='狀態', default=1, index=True)

    donate_total = fields.Integer(string='捐款總額', compute='compute_total',store=True)
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
    payment_method = fields.Selection( selection = [(1,'現金'),(2,'郵政劃撥'),(3,'信用卡扣款'),(4,'銀行轉帳'),(5,'支票')], string='繳費方式', required = True) # 轉檔時, 要把required = True 拿掉
    active = fields.Boolean(default=True)
#    cash = fields.Boolean(string='現金', states={2: [('readonly', True)]})
    person_check = fields.Many2many(comodel_name="normal.p", string="捐款人名冊")
    family_check = fields.One2many(comodel_name='donate.family.line',inverse_name='parent_id', string='捐款人名冊', states={2: [('readonly', True)]})
    donate_list = fields.One2many(comodel_name='donate.order', inverse_name='donate_list_id', string='捐款明細', states={2: [('readonly', True)]})
    work_id = fields.Many2one(comodel_name='cashier.base', string='收費員', states={2: [('readonly', True)]},required = True) # 轉檔時, 要把required = True 拿掉
    temp_work_id = fields.Char(string='收費員')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', states={2: [('readonly', True)]}, default=lambda self: self.env.uid)

    temp_key_in_user = fields.Char(string='輸入人員')

    print_user = fields.Many2one(comodel_name='res.users', string='列印人員', states={2: [('readonly', True)]})
    ps = fields.Text('備註')
    year_fee = fields.Boolean(string='年繳')

    debit_method = fields.Selection(selection=[(1, '5日扣款'), (2, '20日扣款'), (3, '季日扣款'), (4, '年繳扣款'), (5, '單次扣款')],
                                    string='信用卡扣款方式')

    history_donate_flag = fields.Boolean(string='是否上次捐款')
#    history_payment_method = fields.Boolean('是否上次捐款方式')
    report_price_big = fields.Char(string='報表用大寫金額')
    report_donate = fields.Char(string='報表用捐款日期')
    donate_date = fields.Date('捐款日期', index = True, required = True) # 轉檔時, 要把required = True 拿掉
    sreceipt_number = fields.Integer(string='收據筆數', compute='compute_total', store=True)
    print_count = fields.Integer(string='列印筆數',store=True)
    print_date = fields.Date('列印日期')
    donate_family_list = fields.Char('眷屬列表',compute='compute_family_list')
    print_all_donor_list = fields.Boolean(string='列印願意捐助的眷屬')

    clear_all_is_donate = fields.Boolean(string='清除 [是否捐助]')
    clear_all_is_merge = fields.Boolean(string='清除 [是否合併收據]')
    set_today = fields.Boolean(string='今天')

    last_donate_date = fields.Date('上次捐款日期')
    last_donate_type = fields.Selection(selection=[(01, '造橋'), (02, '補路'), (03, '施棺'), (05, '貧困扶助'), (06, '一般捐款')],string='捐款種類')
    cashier_name = fields.Char(string='normal_p的收費員')
    donor_show = fields.Boolean(string='只顯示捐款眷屬', default = True)

    @api.depends('donate_list')
    def compute_total(self):
        for line in self:
            temp_money = 0
            for row in line.donate_list:
                temp_money += row.donate

            line.sreceipt_number += 1
            line.donate_total = temp_money

    @api.onchange('set_today')
    def set_today_donate(self):
        if self.set_today == True:
            self.donate_date = datetime.date.today()
        if self.set_today == False:
            user = self.env['res.users'].search([('login', '=', self.env.user.login)])
            self.donate_date = user.last_donate_date

    @api.onchange('clear_all_is_donate')
    def donate_anti_election(self):
        if self.clear_all_is_donate:
            for line in self.family_check:
                line.is_donate = False
        elif self.clear_all_is_donate is False:
            for line in self.family_check:
                line.is_donate = line.donate_member.is_donate

    @api.onchange('clear_all_is_merge')
    def merge_anti_election(self):
        if self.clear_all_is_merge:
            for line in self.family_check:
                line.is_merge = False
        elif self.clear_all_is_merge is False:
            for line in self.family_check:
                line.is_merge = line.donate_member.is_merge

    def print_check(self,ids):
        res = []
        for line in ids:
            res.append([4, line])
            wizard_data = self.env['print.check'].create({
            'from_target': res
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'print.check',
            'name': '補單確認',
            'view_mode': 'form',
            'res_id': wizard_data.id,
            'target': 'new',
        }

    def bring_last_history(self):
        max_paid = 0
        max = None
        for line in self.donate_member.donate_history_ids:
            if max_paid < int(line.paid_id) and line.state == 1:
                max_paid = int(line.paid_id)
                max = line


        donate_group = self.env['donate.order'].search([('donate_id', '=', max.donate_id)])
        self.family_check.unlink()
        r = []
        exist = []
        for line in donate_group:
            exist_record = False
            for ex_line in exist:
                if ex_line == line.donate_member.id:
                    exist_record = True
            if exist_record is False:
                exist.append(line.donate_member.id)
                r.append([0, 0, {
                    'donate_member': line.donate_member.id
                }])

        self.write({
            'family_check': r
        })
        max = self.env['donate.order'].search([], order='paid_id desc', limit=1)
        max_int = int(max.paid_id) + 1
        for line in donate_group:
            line.write({
                'donate_id': self.donate_id,
                'paid_id': max_int
            })
            max_int += 1
        self.donate_list = donate_group

    @api.model
    def create(self, vals):
        res_id = super(DonateSingle, self).create(vals)
        i = res_id.current_donate_people
        donate_date = datetime.date.today().strftime('%Y-%m-%d')

        historical_data_year = str(datetime.datetime.strptime(donate_date, '%Y-%m-%d').year) # 根據捐款日期取出捐款的年份
        historical_data_month = str(datetime.datetime.strptime(donate_date, '%Y-%m-%d').month) # 根據捐款日期取出捐款的月份
        datas = self.env['donate.statistics'].search([('year','=',historical_data_year),('month','=',historical_data_month)]) # 搜尋計數器中有沒有資料
        if datas: # 如果有找到資料
            receipt_number = datas.receipt_number + 1
            res_id.write({
                'donate_id': 'A' + str(historical_data_year)[2:] + str(historical_data_month).zfill(2) + str(receipt_number).zfill(5),
                'year_fee': res_id.year_fee,
            })
            datas.receipt_number = receipt_number # 捐款的收據張數寫回計數器
            datas.number = datas.number + i # 捐款人數要寫回計數器
        else: # 如果沒有找到資料
            self.env['donate.statistics'].create({
                'year': historical_data_year,
                'month': historical_data_month,
                'receipt_number' : 1,
                'number' : i
            })
            receipt_number = 1
            res_id.write({
                'donate_id': 'A' + str(historical_data_year)[2:] + str(historical_data_month).zfill(2) + str(receipt_number).zfill(5),
                'year_fee': res_id.year_fee
            })

        self.add_to_list_create(res_id)
        for line in res_id.donate_member.donate_family1:
            if line.is_donate is True:
                line.last_donate_date = res_id.donate_date

        donate_user = self.env['normal.p'].search([('id', '=', res_id.donate_member.id)])
        donate_user.write({
            'rec_send':res_id.receipt_send, #收據寄送
            'report_send':res_id.report_send, #報表寄送
            'merge_report':res_id.year_receipt_send, #年收據合併 開始捐款(年收據寄送) 已將年收據合併改為年收據寄送
            'print_all_donor_list':res_id.print_all_donor_list,
            'last_donate_date':res_id.donate_date # 上次捐款時間
        })

        user = self.env['res.users'].search([('login', '=', self.env.user.login)])

        user.write({
            'payment_method':res_id.payment_method,
            'last_donate_date':res_id.donate_date
        })
        return res_id

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('donate_member_w_id', operator, name), '|', ('donate_member_new_coding', operator, name)]
        banks = self.search(domain + args, limit=limit)
        return banks.name_get()


    @api.onchange('history_donate_flag')
    def get_history_donate(self):

        if self.history_donate_flag is True:
            max = None
            second_last = len(self.donate_member.donate_single_history_ids)
            for line in self.donate_member.donate_single_history_ids[0:second_last - 1]:
                max = line
            if max:
                old = self.search([('donate_id', '=', max.donate_id)])
                r = []
                for line in old.family_check:
                    r.append([0, 0, {
                        'donate_member': line.donate_member.id
                    }])

                self.update({
                    'family_check': r,
                    'bridge': old.bridge,
                    'bridge_money': old.bridge_money,
                    'road': old.road,
                    'road_money': old.road_money,
                    'coffin': old.coffin,
                    'coffin_money': old.coffin_money,
                    'poor_help': old.poor_help,
                    'poor_help_money': old.poor_help_money,
                    'noassign': old.noassign,
                    'noassign_money': old.noassign_money,
                })
            else:
                raise ValidationError(u'系統查詢結果並無歷史捐款紀錄')

    @api.onchange('family_check')
    def current_people(self):
        self.current_donate_people = 0
        self.current_donate_total = 0
        self.current_donate_project = 0
        for line in self.family_check:
            if line.is_donate is True:
                self.current_donate_people += 1
                if line.bridge_money != 0:
                    self.current_donate_project += 1
                    self.current_donate_total += line.bridge_money
                if line.road_money != 0:
                    self.current_donate_project += 1
                    self.current_donate_total += line.road_money
                if line.coffin_money != 0:
                    self.current_donate_project += 1
                    self.current_donate_total += line.coffin_money
                if line.poor_help_money != 0:
                    self.current_donate_project += 1
                    self.current_donate_total += line.poor_help_money
                if line.noassign_money != 0:
                    self.current_donate_project += 1
                    self.current_donate_total += line.noassign_money
            elif line.is_donate is False:
                line.bridge_money = 0
                line.road_money = 0
                line.coffin_money = 0
                line.poor_help_money = 0
                line.noassign_money = 0


    @api.onchange('bridge_money','road_money','coffin_money','poor_help_money','noassign_money')
    def compute_donate_total(self):
        self.current_donate_total = 0
        if self.family_check:
            for line in self.family_check.filtered(lambda  x :x.is_donate==True):
                if self.bridge_money != 0:
                    line.bridge_money = self.bridge_money
                elif self.bridge_money == 0:
                    if line.bridge_money != 0:
                        line.bridge_money = self.bridge_money
                if self.road_money != 0:
                    line.road_money = self.road_money
                elif self.road_money == 0:
                    if line.road_money != 0:
                        line.road_money = self.road_money
                if self.coffin_money != 0:
                    line.coffin_money = self.coffin_money
                elif self.coffin_money == 0:
                    if line.coffin_money != 0:
                        line.coffin_money = self.coffin_money
                if self.poor_help_money != 0:
                    line.poor_help_money = self.poor_help_money
                elif self.poor_help_money == 0:
                    if line.poor_help_money !=0:
                        line.poor_help_money = self.poor_help_money
                if self.noassign_money != 0:
                    line.noassign_money = self.noassign_money
                elif self.noassign_money == 0:
                    if line.noassign_money != 0:
                        line.noassign_money = self.noassign_money


        for line in self.family_check:
            if line.is_donate is True:
                if line.bridge_money !=0:
                    self.bridge = True
                if line.road_money !=0:
                    self.road = True
                if line.coffin_money !=0:
                    self.coffin = True
                if line.poor_help_money !=0:
                    self.poor_help = True
                if line.noassign_money !=0:
                    self.noassign = True
                self.current_donate_total += line.bridge_money
                self.current_donate_total += line.road_money
                self.current_donate_total += line.coffin_money
                self.current_donate_total += line.poor_help_money
                self.current_donate_total += line.noassign_money

        self.donate_total = self.current_donate_total

    @api.onchange('donate_member','donor_show')
    def show_family(self):
        r = []
        family=None
        if self.donor_show :
            family = self.donate_member.parent.donate_family1.filtered(lambda r: r.is_donate)
        else:
            family = self.donate_member.parent.donate_family1
        for line in family:
            r.append([0, 0, {
                'donate_member': line.id
            }])
        self.update({
            'family_check': r,
            'work_id':self.donate_member.cashier_name.id
        })
        user = self.env['res.users'].search([('login', '=', self.env.user.login)])
        self.payment_method = user.payment_method
        self.donate_date = user.last_donate_date



    @api.depends('donate_list')
    def compute_family_list(self):
        for line in self:
            str = ''
            for row in line.donate_list:
                if row.donate_type == 1:
                    str +=  " (%s %s %s )," % (row.donate_member.name, u'造橋',row.donate)
                if row.donate_type == 2:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'補路',row.donate)
                if row.donate_type == 3:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'施棺',row.donate)
                if row.donate_type == 4:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'伙食費',row.donate)
                if row.donate_type == 5:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'貧困扶助',row.donate)
                if row.donate_type == 6:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'一般捐款',row.donate)
                if row.donate_type == 99:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'其他工程',row.donate)
            line.donate_family_list= str.rstrip(',')

    # 新建立捐款在眷屬列表顯示個人姓名+捐款種類+捐款金額
    def compute_family_list_create(self):
        for line in self:
            str = ''
            for row in line.donate_list:
                if row.donate_type == 1:
                    str +=  " (%s %s %s )," % (row.donate_member.name, u'造橋',row.donate)
                if row.donate_type == 2:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'補路',row.donate)
                if row.donate_type == 3:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'施棺',row.donate)
                if row.donate_type == 4:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'伙食費',row.donate)
                if row.donate_type == 5:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'貧困扶助',row.donate)
                if row.donate_type == 6:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'一般捐款',row.donate)
                if row.donate_type == 99:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'其他工程',row.donate)
            line.donate_family_list= str.rstrip(',')

    def button_to_cnacel_donate(self):
        single_data = self.env['wizard.abandon.single'].create({
            'donate_single_code': self.id
        })
        action = self.env.ref('cdg_base.action_wizard_abandon_single').read()[0]
        action['res_id'] = single_data.id
        return action

    def change_print_state(self):
        if self.state == 3:
            raise ValidationError(u'本捐款單已作廢!!')

        self.state = 1


    def add_to_list_create(self, record):
        if record.family_check:
            for line in record.family_check.filtered(lambda  x :x.is_donate==True):
                if record.print_all_donor_list:
                    if line.bridge_money == 0 and line.road_money == 0 and line.coffin_money == 0 and line.poor_help_money == 0 and line.noassign_money == 0:
                        record.save_donate_list(6, line.donate_member, line.noassign_money)
                    if line.bridge_money != 0:
                        record.save_donate_list(1, line.donate_member, line.bridge_money)
                    if line.road_money != 0:
                        record.save_donate_list(2, line.donate_member, line.road_money)
                    if line.coffin_money != 0:
                        record.save_donate_list(3, line.donate_member, line.coffin_money)
                    if line.poor_help_money != 0:
                        record.save_donate_list(5, line.donate_member, line.poor_help_money)
                    if line.noassign_money != 0:
                        record.save_donate_list(6, line.donate_member, line.noassign_money)
                else:
                    if line.bridge_money != 0:
                        record.save_donate_list(1, line.donate_member, line.bridge_money)
                    if line.road_money != 0:
                        record.save_donate_list(2, line.donate_member, line.road_money)
                    if line.coffin_money != 0:
                        record.save_donate_list(3, line.donate_member, line.coffin_money)
                    if line.poor_help_money != 0:
                        record.save_donate_list(5, line.donate_member, line.poor_help_money)
                    if line.noassign_money != 0:
                        record.save_donate_list(6, line.donate_member, line.noassign_money)
        else:
            raise ValidationError(u'捐款名冊為空，無法進行捐款作業')


    def add_to_list(self):
        # 將明細產生按鈕執行
        self.donate_list.unlink()
        if self.family_check:
            for line in self.family_check.filtered(lambda  x :x.is_donate==True):
                if line.bridge_money != 0:
                    self.save_donate_list(1, line.donate_member, line.bridge_money)
                if line.road_money != 0:
                    self.save_donate_list(2, line.donate_member, line.road_money)
                if line.coffin_money != 0:
                    self.save_donate_list(3, line.donate_member, line.coffin_money)
                if line.poor_help_money != 0:
                    self.save_donate_list(5, line.donate_member, line.poor_help_money)
                if line.noassign_money != 0:
                    self.save_donate_list(6, line.donate_member, line.noassign_money)
                if self.print_all_donor_list and (line.bridge_money == 0 and line.road_money == 0 and line.coffin_money == 0 and line.poor_help_money == 0 and line.noassign_money == 0 ):
                    self.save_donate_list(6, line.donate_member, line.noassign_money)
        else:
            raise ValidationError(u'捐款名冊為空，無法進行捐款作業')


    def save_donate_list(self, donate_type, member_id, money):  # 將明細產生

        if donate_type == 3:
            self.write({
                'donate_list': [(0, 0, {
                    'donate_id': self.donate_id,
                    'donate_member': member_id.id,
                    'donate_type': donate_type,
                    'donate': money,
                    'donate_date': self.donate_date,
                    'self_id': member_id.self_iden,
                    'payment_method': int(self.payment_method),
                    'available_balance': money,
                    'key_in_user': self.key_in_user.id,
                    'cashier':self.work_id.id,
                    'debit_method': self.debit_method,
                })],
                'print_all_donor_list': self.print_all_donor_list
            })
        else:
            self.write({
                'donate_list': [(0, 0, {
                    'donate_id': self.donate_id,
                    'donate_member': member_id.id,
                    'donate_type': donate_type,
                    'donate': money,
                    'donate_date':self.donate_date,
                    'self_id': member_id.self_iden,
                    'payment_method': int(self.payment_method),
                    'key_in_user': self.key_in_user.id,
                    'cashier': self.work_id.id,
                    'debit_method': self.debit_method,
                })],
                'print_all_donor_list': self.print_all_donor_list
            })

    def parent_list_creat(self):
        r = []
        for line in self.donate_member.parent.donate_family1:
            exist = False
            for family_line in self.family_check:
                if family_line.donate_member.id == line.id:
                    exist = True

            if exist is False:
                r.append([0, 0, {
                    'donate_member': line.id
                }])

        self.write({
            'family_check': r
        })
        self.donate_list.unlink()

    @api.depends('donate_member')
    def set_donate_name(self):
        for line in self:
            normal_p = line.donate_member
            line.name = normal_p.name
            line.donate_member_w_id = normal_p.w_id
            line.donate_member_number = normal_p.number
            line.cellpnone = normal_p.cellphone
            line.con_phone = normal_p.con_phone
            line.self_iden = normal_p.self_iden
            line.zip_code = normal_p.zip_code
            line.con_addr = normal_p.con_addr
            line.zip = normal_p.zip
            line.rec_addr = normal_p.rec_addr
            line.receipt_send = normal_p.rec_send
            line.report_send = normal_p.report_send
            line.year_receipt_send = normal_p.merge_report
            line.print_all_donor_list = normal_p.print_all_donor_list
            line.ps = normal_p.ps

    def start_donate(self):
        action = self.env.ref('cdg_base.start_donate_action').read()[0]
        user = self.env['res.users'].search([('login', '=', self.env.user.login)])
        action['context'] = {'default_donate_member':self.donate_member.id, 'default_payment_method':user.payment_method}
        return action

class DonateSingleLine(models.Model):
    _name = 'donate.family.line'
    _order = 'sequence'

    parent_id = fields.Many2one(comodel_name='donate.single', index = True)
    family_new_coding = fields.Char(string='捐款者編號',related='donate_member.new_coding', readonly=True)
    donate_member = fields.Many2one(comodel_name='normal.p', string='捐款人', index = True)
    is_donate = fields.Boolean(string='是否捐助', related='donate_member.is_donate')
    is_merge = fields.Boolean(string='是否合併收據', related='donate_member.is_merge')

    bridge_money = fields.Integer(string='造橋')
    road_money = fields.Integer(string='補路')
    coffin_money = fields.Integer(string='施棺')
    poor_help_money = fields.Integer(string='貧困扶助')
    noassign_money = fields.Integer(string='一般捐款')

    sequence = fields.Integer(string='排序', related='donate_member.sequence')
