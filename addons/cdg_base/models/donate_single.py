# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging, datetime
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class DonateSingle(models.Model):
    _name = 'donate.single'
    _rec_name = 'donate_id'

    # name = fields.Many2one(comodel_name='normal.p',string='姓名')

    paid_id = fields.Char(string='收費編號', readonly=True)
    donate_id = fields.Char(string='收據編號', readonly=True)
    donate_member = fields.Many2one(comodel_name='normal.p', string='捐款者',
                                    states={2: [('readonly', True)]})  # demo用
    w_id = fields.Char('舊團員編號', related='donate_member.w_id')  # 歷史捐款明細智慧按鈕需要用的, 拿掉就掛了
    new_coding = fields.Char('新捐款者編號', related='donate_member.new_coding')  # 歷史捐款明細智慧按鈕需要用的, 拿掉就掛了

    donate_member_w_id = fields.Char('舊團員編號',related='donate_member.w_id') # search用   (轉檔時, 要把 related 去掉)
    donate_member_number = fields.Char('舊團員序號',related='donate_member.number') # 轉檔時, 要把 related 去掉

    donate_member_new_coding = fields.Char('新捐款者編號',related='donate_member.new_coding')  # search用
    name = fields.Char(string='姓名', compute='set_donate_name',store=True)
    self_iden = fields.Char(string='身分證字號', compute='set_donate_name', store=True)
    cellphone = fields.Char(string='手機', compute='set_donate_name', store=True)
    con_phone = fields.Char(string='聯絡電話', compute='set_donate_name', store=True)
    zip_code = fields.Char(string='郵遞區號', compute='set_donate_name', store=True)
    con_addr = fields.Char(string='聯絡地址', compute='set_donate_name', store=True)

    state = fields.Selection([(1, '已產生'), (2, '已列印'), (3, '已作廢')],
                             string='狀態', default=1, index=True)

    donate_total = fields.Integer(string='捐款總額', compute='compute_total')
    current_donate_total = fields.Integer('目前捐款總額', readonly="1")
    current_donate_people = fields.Integer('目前捐款人數', readonly="1")

    old_donate_total = fields.Integer(string='舊捐款總額')

    receipt_send = fields.Boolean(string='收據寄送')
    report_send = fields.Boolean(string='報表寄送')
    year_receipt_send = fields.Boolean(string='年收據寄送')
    bridge = fields.Boolean(string='造橋')
    road = fields.Boolean(string='補路')
    coffin = fields.Boolean(string='施棺')
    poor_help = fields.Boolean(string='貧困扶助')
    noassign = fields.Boolean(string='不指定')
    bridge_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    road_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    coffin_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    poor_help_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    noassign_money = fields.Integer(string='$', states={2: [('readonly', True)]})
    payment_method = fields.Selection( [(1,'現金'),(2,'郵政劃撥'),(3,'信用卡扣款'),(4,'銀行轉帳'),(5,'支票')], string='繳費方式')
#    cash = fields.Boolean(string='現金', states={2: [('readonly', True)]})
    person_check = fields.Many2many(comodel_name="normal.p", string="捐款人名冊")
    family_check = fields.One2many(comodel_name='donate.family.line',inverse_name='parent_id', string='捐款人名冊', states={2: [('readonly', True)]})
    donate_list = fields.One2many(comodel_name='donate.order', inverse_name='donate_list_id', string='捐款明細', states={2: [('readonly', True)]})
    work_id = fields.Many2one(comodel_name='cashier.base', string='收費員', states={2: [('readonly', True)]})
    temp_work_id = fields.Char(string='收費員')
    key_in_user = fields.Many2one(comodel_name='res.users', string='輸入人員', states={2: [('readonly', True)]}, default=lambda self: self.env.uid)
    temp_key_in_user = fields.Char(string='輸入人員')
    print_user = fields.Many2one(comodel_name='res.users', string='列印人員', states={2: [('readonly', True)]})


    history_donate_flag = fields.Boolean(string='是否上次捐款')
#    history_payment_method = fields.Boolean('是否上次捐款方式')
    report_price_big = fields.Char(string='報表用大寫金額')
    report_donate = fields.Char(string='報表用捐款日期')
    donate_date = fields.Date('捐款日期')
    sreceipt_number = fields.Integer(string='收據筆數', compute='compute_total', store=True)
    print_count = fields.Integer(string='列印筆數',store=True)
    print_date = fields.Date('列印日期')
    donate_family_list = fields.Char('眷屬列表',compute='compute_family_list')

    clear_all_is_donate = fields.Boolean(string='清除 [是否捐助]')
    clear_all_is_merge = fields.Boolean(string='清除 [是否合併收據]')

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
        if res_id.donate_member.id is False:
            raise ValidationError(u'需要選取捐款人!')
        elif res_id.payment_method is not 1 and res_id.payment_method is not 2 and res_id.payment_method is not 3 and res_id.payment_method is not 4:
            raise ValidationError(u'支付方法至少選取一個')
        elif res_id.work_id.name is False:
            raise ValidationError(u'必須選取收費員')

        i = 0
        is_donate_flag = False
        for line in res_id.family_check: # 計算該捐款者眷屬有多少人是願意捐款的
            if line.is_donate:
                is_donate_flag = True
                i = i + 1
        if not is_donate_flag:
            raise ValidationError(u'請至少有一人需要捐款')

        historical_data_year = str(datetime.datetime.strptime(res_id.donate_date, '%Y-%m-%d').year) # 根據捐款日期取出捐款的年份
        historical_data_month = str(datetime.datetime.strptime(res_id.donate_date, '%Y-%m-%d').month) # 根據捐款日期取出捐款的月份
        datas = self.env['donate.statistics'].search([('year','=',historical_data_year),('month','=',historical_data_month)]) # 搜尋計數器中有沒有資料
        if datas: # 如果有找到資料
            receipt_number = datas.receipt_number + 1
            res_id.write({
                'donate_id': 'A' + str(historical_data_year)[2:] + str(historical_data_month).zfill(2) + str(receipt_number).zfill(5)
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
                'donate_id': 'A' + str(historical_data_year)[2:] + str(historical_data_month).zfill(2) + str(receipt_number).zfill(5)
            })

        self.add_to_list_create(res_id)
        self.compute_family_list_create()

        #donate_single(Create保存).donate_member(normal.p的資料).(欄位) = donate_single.(欄位)
        donate_user = self.env['normal.p'].search([('id', '=', res_id.donate_member.id)])
        donate_user.rec_send = res_id.receipt_send #收據寄送
        donate_user.report_send = res_id.report_send #報表寄送
        donate_user.merge_report = res_id.year_receipt_send #年收據合併 開始捐款(年收據寄送) 已將年收據合併改為年收據寄送

        user = self.env['res.users'].search([('login', '=', self.env.user.login)])
        user.payment_method = res_id.payment_method
        user.last_donate_date = res_id.donate_date
        return res_id

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('donate_member_w_id', operator, name), '|', ('donate_member_new_coding', operator, name)]
        banks = self.search(domain + args, limit=limit)
        return banks.name_get()

    # @api.onchange('history_payment_method')
    # def get_history_payment_method(self):
    #     if(self.history_payment_method == True):
    #       last_order = self.env['donate.single'].search([('create_uid', '=', self.env.user.id)])[-1]
    #       self.update({
    #         'payment_method': last_order.payment_method
    #      })



    @api.onchange('history_donate_flag')
    def get_history_donate(self):

        if self.history_donate_flag is True:
            max = None
            second_last = len(self.donate_member.donate_single_history_ids)
            for line in self.donate_member.donate_single_history_ids[0:second_last - 1]:
                max = line
                print(line.donate_id)
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
        for line in self.family_check:
            if line.is_donate is True:
                self.current_donate_people += 1

    @api.onchange('bridge', 'road', 'coffin', 'poor_help','noassign')
    def set_default_price(self):
        self.current_donate_total = 0
        if self.bridge and self.bridge_money == 0:
            self.bridge_money = 100
        elif self.bridge is False:
            self.bridge_money = 0
        if self.road and self.road_money == 0:
            self.road_money = 100
        elif self.road is False:
            self.road_money = 0
        if self.coffin and self.coffin_money == 0:
            self.coffin_money = 100
        elif self.coffin is False:
            self.coffin_money = 0
        if self.poor_help and self.poor_help_money == 0:
            self.poor_help_money = 100
        elif self.poor_help is False:
            self.poor_help_money = 0
        if self.noassign and self.noassign_money == 0:
            self.noassign_money = 100
        elif self.noassign is False:
            self.noassign_money = 0

        for line in self.family_check:
            if line.is_donate is True:
                self.current_donate_total += self.bridge_money
                self.current_donate_total += self.road_money
                self.current_donate_total += self.coffin_money
                self.current_donate_total += self.poor_help_money
                self.current_donate_total += self.noassign_money


    @api.onchange('bridge_money','road_money','coffin_money', 'poor_help_money','noassign_money')
    def set_checkbox_check(self):
        self.current_donate_total = 0
        if self.bridge_money != 0:
            self.bridge = True
        else:
            self.bridge = False
        if self.road_money != 0:
            self.road = True
        else:
            self.road = False
        if self.coffin_money != 0:
            self.coffin = True
        else:
            self.coffin = False
        if self.poor_help_money != 0:
            self.poor_help = True
        else:
            self.poor_help = False
        if self.noassign_money != 0:
            self.noassign = True
        else:
            self.noassign = False

        for line in self.family_check:
            if line.is_donate is True:
                self.current_donate_total += self.bridge_money
                self.current_donate_total += self.road_money
                self.current_donate_total += self.coffin_money
                self.current_donate_total += self.poor_help_money
                self.current_donate_total += self.noassign_money

    @api.onchange('donate_member')
    def show_family(self):
        r = []
        for line in self.donate_member.parent.donate_family1:
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
    def compute_total(self):
        for line in self:
            for row in line.donate_list:
                line.sreceipt_number += 1
                if row.donate_member.is_donate == True:
                    line.donate_total += row.donate

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
                    str += " (%s %s %s )," % (row.donate_member.name,  u'不指定',row.donate)
                if row.donate_type == 99:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'其他工程',row.donate)
            line.donate_family_list= str

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
                    str += " (%s %s %s )," % (row.donate_member.name,  u'不指定',row.donate)
                if row.donate_type == 99:
                    str += " (%s %s %s )," % (row.donate_member.name,  u'其他工程',row.donate)
            line.donate_family_list= str

    def button_to_cnacel_donate(self):
        if self.state == 3:
            raise ValidationError(u'本捐款單已作廢!!')
        elif self.state == 2:
            raise ValidationError(u'本捐款單已列印收據!!')

        for line in self.donate_list:
            if line.used_money != 0:
                raise ValidationError(u'本捐款單的 %s 先生/小姐 施棺捐款 %s 元整，已支出!! 因此無法作廢或退費，感謝您的善心' % (line.donate_member.name, line.donate))

        for line in self.donate_list:
            line.state = 2
        self.state = 3

    def add_to_list_create(self, record):

        max = self.env['donate.order'].search([], order='paid_id desc', limit=1)
        max_int = int(max.paid_id) + 1
        if record.family_check:
            for line in record.family_check.filtered(lambda  x :x.is_donate==True):
                if record.bridge:
                    record.save_donate_list(1, str(max_int), line.donate_member, record.bridge_money)
                    max_int = max_int + 1
                if record.road:
                    record.save_donate_list(2, str(max_int), line.donate_member, record.road_money)
                    max_int = max_int + 1
                if record.coffin:
                    record.save_donate_list(3, str(max_int), line.donate_member, record.coffin_money)
                    max_int = max_int + 1
                if record.poor_help:
                    record.save_donate_list(5, str(max_int), line.donate_member, record.poor_help_money)
                    max_int = max_int + 1
                if record.noassign:
                    record.save_donate_list(6, str(max_int), line.donate_member, record.noassign_money)
                    max_int = max_int + 1
        else:
            if record.bridge:
                record.save_donate_list(1, str(max_int), record.donate_member, record.bridge_money)
                max_int = max_int + 1
            if record.road:
                record.save_donate_list(2, str(max_int), record.donate_member, record.road_money)
                max_int = max_int + 1
            if record.coffin:
                record.save_donate_list(3, str(max_int), record.donate_member, record.coffin_money)
                max_int = max_int + 1
            if record.poor_help:
                record.save_donate_list(5, str(max_int), record.donate_member, record.poor_help_money)
                max_int = max_int + 1
            if record.noassign:
                record.save_donate_list(6, str(max_int), record.donate_member, record.noassign_money)
                max_int = max_int + 1

    def add_to_list(self):
        # 將明細產生按鈕執行
        self.donate_list.unlink()
        max = self.env['donate.order'].search([], order='paid_id desc', limit=1)
        max_int = int(max.paid_id) + 1
        if self.family_check:
            for line in self.family_check.filtered(lambda  x :x.is_donate==True):
                if self.bridge:
                    self.save_donate_list(1, str(max_int), line.donate_member, self.bridge_money)
                    max_int = max_int + 1
                if self.road:
                    self.save_donate_list(2, str(max_int), line.donate_member, self.road_money)
                    max_int = max_int + 1
                if self.coffin:
                    self.save_donate_list(3, str(max_int), line.donate_member, self.coffin_money)
                    max_int = max_int + 1
                if self.poor_help:
                    self.save_donate_list(5, str(max_int), line.donate_member, self.poor_help_money)
                    max_int = max_int + 1
                if self.noassign:
                    self.save_donate_list(6, str(max_int), line.donate_member, self.noassign_money)
                    max_int = max_int + 1
        else:
            if self.bridge:
                self.save_donate_list(1, str(max_int), self.donate_member, self.bridge_money)
                max_int = max_int + 1
            if self.road:
                self.save_donate_list(2, str(max_int), self.donate_member, self.road_money)
                max_int = max_int + 1
            if self.coffin:
                self.save_donate_list(3, str(max_int), self.donate_member, self.coffin_money)
                max_int = max_int + 1
            if self.poor_help:
                self.save_donate_list(5, str(max_int), self.donate_member, self.poor_help_money)
                max_int = max_int + 1
            if self.noassign:
                self.save_donate_list(6, str(max_int), self.donate_member, self.noassign_money)
                max_int = max_int + 1

    def save_donate_list(self, donate_type, paid_id, member_id, money):  # 將明細產生
        if donate_type == 3:
            self.write({
                'donate_list': [(0, 0, {
                    'donate_id': self.donate_id,
                    'paid_id': str(paid_id),
                    'donate_member': member_id.id,
                    'donate_type': donate_type,
                    'donate': money,
                    'donate_date': datetime.date.today(),
                    'self_id': member_id.self_iden,
                    'payment_method': int(self.payment_method),
                    'available_balance': money
                })]
            })
        else:
            self.write({
                'donate_list': [(0, 0, {
                    'donate_id': self.donate_id,
                    'paid_id': str(paid_id),
                    'donate_member': member_id.id,
                    'donate_type': donate_type,
                    'donate': money,
                    'donate_date': datetime.date.today(),
                    'self_id': member_id.self_iden,
                    'payment_method': int(self.payment_method),
                })]
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
            line.receipt_send = normal_p.rec_send
            line.report_send = normal_p.report_send
            line.year_receipt_send = normal_p.merge_report

    def start_donate(self):
        action = self.env.ref('cdg_base.start_donate_action').read()[0]
        user = self.env['res.users'].search([('login', '=', self.env.user.login)])
        action['context'] = {'default_donate_member':self.donate_member.id, 'default_payment_method':user.payment_method}
        return action


class DonateSingleLine(models.Model):
    _name = 'donate.family.line'

    parent_id = fields.Many2one(comodel_name='donate.single')
    family_new_coding = fields.Char(string='捐款者編號',related='donate_member.new_coding', readonly=True)
    donate_member = fields.Many2one(comodel_name='normal.p', string='捐款人')
    is_donate = fields.Boolean(string='是否捐助', related='donate_member.is_donate')
    is_merge = fields.Boolean(string='是否合併收據', related='donate_member.is_merge')

    bridge_money = fields.Integer(string='造橋')
    road_money = fields.Integer(string='補路')
    coffin_money = fields.Integer(string='施棺')
    poor_help_money = fields.Integer(string='貧困扶助')
    noassign_money = fields.Integer(string='不指定')
